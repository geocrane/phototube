import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .constants import (
    ANOTHER_FOLLOW_URL,
    ANOTHER_GROUP_URL,
    ANOTHER_PROFILE_URL,
    ANOTHER_SLUG,
    ANOTHER_USER,
    FOLLOW_URL,
    FOLLOW_INDEX_URL,
    FOLLOW_INDEX_URL_PAGE2,
    UNFOLLOW_URL,
    GROUP_URL,
    GROUP_URL_PAGE2,
    INDEX_URL,
    INDEX_URL_PAGE2,
    PROFILE_URL,
    PROFILE_URL_PAGE2,
    SMALL_GIF,
    TEST_USER,
    TEST_SLUG,
)
from ..models import Follow, Group, Post, User
from phototube.settings import POSTS_ON_PAGE

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(TEST_USER)
        cls.follower = User.objects.create_user(ANOTHER_USER)
        cls.group = Group.objects.create(
            title="TestGroup",
            slug=TEST_SLUG,
            description="TestDescription",
        )
        cls.another_group = Group.objects.create(
            title="AnotherGroup",
            slug=ANOTHER_SLUG,
            description="AnotherDescription",
        )
        cls.uploaded = SimpleUploadedFile(
            name="test.gif", content=SMALL_GIF, content_type="posts/small.gif"
        )
        cls.post = Post.objects.create(
            text="Текст поста",
            author=cls.user,
            group=cls.group,
            image=cls.uploaded,
        )
        Follow.objects.create(user=cls.follower, author=cls.user)
        cls.POST_DETAIL_URL = reverse("posts:post_detail", args=[cls.post.id])
        cls.POST_EDIT_URL = reverse("posts:post_edit", args=[cls.post.id])

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.follower_client = Client()
        cls.follower_client.force_login(cls.follower)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_post_shows_correct_on_index_gtoup_profile_detail(self):
        """Пост отображается на index, group, profile, post_detail, follow"""
        urls_context = {
            INDEX_URL: "page_obj",
            GROUP_URL: "page_obj",
            PROFILE_URL: "page_obj",
            FOLLOW_INDEX_URL: "page_obj",
            self.POST_DETAIL_URL: "post",
        }
        for url, context in urls_context.items():
            with self.subTest(url=url):
                response = self.follower_client.get(url)
                if context == "page_obj":
                    self.assertEqual(len(response.context[context]), 1)
                    post = response.context[context][0]
                else:
                    post = response.context[context]
                self.assertEqual(post, self.post)
                self.assertEqual(post.text, self.post.text)
                self.assertEqual(post.group, self.post.group)
                self.assertEqual(post.author, self.post.author)
                self.assertEqual(post.image, self.post.image)

    def test_posts_filtered_group_author(self):
        """Посты отфильтрованы по группе, автору и подпискам"""
        urls = [ANOTHER_GROUP_URL, ANOTHER_PROFILE_URL, FOLLOW_INDEX_URL]
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertNotIn(self.post, response.context["page_obj"])

    def test_group_context(self):
        """Группа в контексте group_posts без искажения атрибутов"""
        group = self.authorized_client.get(GROUP_URL).context["group"]
        self.assertEqual(group, self.group)
        self.assertEqual(group.title, self.group.title)
        self.assertEqual(group.slug, self.group.slug)
        self.assertEqual(group.description, self.group.description)

    def test_profile_context_author(self):
        """Присутствует автор в контексте profile"""
        author = self.authorized_client.get(PROFILE_URL).context["author"]
        self.assertEqual(self.user, author)

    def test_user_can_unfollow(self):
        """Пользователь может отписаться от автора"""
        self.follower_client.get(UNFOLLOW_URL)
        self.assertFalse(
            Follow.objects.filter(
                user=self.follower, author=self.user
            ).exists()
        )

    def test_user_can_follow(self):
        """Пользователь может подписаться на автора"""
        self.authorized_client.get(ANOTHER_FOLLOW_URL)
        self.assertTrue(
            Follow.objects.filter(
                user=self.user, author=self.follower
            ).exists()
        )

    def test_user_cant_follow_self(self):
        """Пользователь не может подписаться на себя"""
        self.authorized_client.get(FOLLOW_URL)
        self.assertFalse(
            Follow.objects.filter(
                user=self.user, author=self.user
            ).exists()
        )

    def test_cash_on_index(self):
        """Тест кэша в шаблоне index"""
        content_before = self.authorized_client.get(INDEX_URL).content
        Post.objects.all().delete()
        content_after = self.authorized_client.get(INDEX_URL).content
        self.assertEqual(content_before, content_after)
        cache.clear()
        content_after_clear = self.authorized_client.get(INDEX_URL).content
        self.assertNotEqual(content_before, content_after_clear)

    def test_paginator(self):
        """Паджинатор отображается на index, group, profile, follow"""
        posts_before = Post.objects.all().count()
        Post.objects.bulk_create(
            Post(
                text=f"Some post text №{i}", author=self.user, group=self.group
            )
            for i in range(POSTS_ON_PAGE)
        )
        posts_on_last_page = (POSTS_ON_PAGE + posts_before) % POSTS_ON_PAGE
        paginator_cases = [
            [INDEX_URL, POSTS_ON_PAGE],
            [GROUP_URL, POSTS_ON_PAGE],
            [PROFILE_URL, POSTS_ON_PAGE],
            [FOLLOW_INDEX_URL, POSTS_ON_PAGE],
            [INDEX_URL_PAGE2, posts_on_last_page],
            [GROUP_URL_PAGE2, posts_on_last_page],
            [PROFILE_URL_PAGE2, posts_on_last_page],
            [FOLLOW_INDEX_URL_PAGE2, posts_on_last_page],
        ]
        for url, value in paginator_cases:
            with self.subTest(url=url):
                self.assertEqual(
                    len(self.follower_client.get(url).context["page_obj"]),
                    value,
                )

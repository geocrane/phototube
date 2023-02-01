from http.client import FOUND, NOT_FOUND, OK

from django.test import Client, TestCase
from django.urls import reverse

from .constants import (
    ANOTHER_USER,
    CREATE_REDIRECT,
    FOLLOW_REDIRECT,
    GROUP_URL,
    INDEX_URL,
    FOLLOW_INDEX_URL,
    FOLLOW_URL,
    LOGIN_URL,
    POST_CREATE_URL,
    PROFILE_URL,
    TEST_SLUG,
    TEST_USER,
    UNFOLLOW_URL,
    UNFOLLOW_REDIRECT
)
from ..models import Group, Post, User


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(TEST_USER)
        cls.not_author = User.objects.create_user(ANOTHER_USER)
        cls.group = Group.objects.create(
            title="TestGroup",
            slug=TEST_SLUG,
            description="TestDescription",
        )

        cls.post = Post.objects.create(
            text="Тестовый текст поста",
            author=cls.author,
            group=cls.group,
        )
        cls.POST_DETAIL_URL = reverse("posts:post_detail", args=[cls.post.id])
        cls.POST_EDIT_URL = reverse("posts:post_edit", args=[cls.post.id])
        cls.EDIT_LOGIN = f"{LOGIN_URL}?next={cls.POST_EDIT_URL}"

        cls.guest = Client()
        cls.authorized = Client()
        cls.authorized.force_login(cls.author)
        cls.another = Client()
        cls.another.force_login(cls.not_author)

    def test_pages_response(self):
        """Ответ страниц на запросы"""
        cases = [
            [INDEX_URL, self.authorized, OK],
            [GROUP_URL, self.authorized, OK],
            [PROFILE_URL, self.authorized, OK],
            [POST_CREATE_URL, self.authorized, OK],
            [POST_CREATE_URL, self.guest, FOUND],
            [self.POST_DETAIL_URL, self.authorized, OK],
            [self.POST_EDIT_URL, self.authorized, OK],
            [self.POST_EDIT_URL, self.another, FOUND],
            [self.POST_EDIT_URL, self.guest, FOUND],
            [FOLLOW_INDEX_URL, self.authorized, OK],
            [FOLLOW_URL, self.authorized, FOUND],
            [FOLLOW_URL, self.another, FOUND],
            [FOLLOW_URL, self.guest, FOUND],
            [UNFOLLOW_URL, self.authorized, NOT_FOUND],
            [UNFOLLOW_URL, self.another, FOUND],
            [UNFOLLOW_URL, self.guest, FOUND],
            ["/unexcisting_page/", self.authorized, NOT_FOUND],
        ]
        for url, client, status in cases:
            with self.subTest(url=url, client=client):
                URLTests.assertEqual(
                    self, client.get(url).status_code, status
                )

    def test_redirect_pages(self):
        """Перенаправления страниц"""
        cases = [
            [POST_CREATE_URL, self.guest, CREATE_REDIRECT],
            [self.POST_EDIT_URL, self.guest, self.EDIT_LOGIN],
            [self.POST_EDIT_URL, self.another, self.POST_DETAIL_URL],
            [FOLLOW_URL, self.authorized, PROFILE_URL],
            [FOLLOW_URL, self.guest, FOLLOW_REDIRECT],
            [FOLLOW_URL, self.another, PROFILE_URL],
            [UNFOLLOW_URL, self.another, PROFILE_URL],
            [UNFOLLOW_URL, self.guest, UNFOLLOW_REDIRECT],
        ]
        for url, client, redirect in cases:
            with self.subTest(url=url, client=client):
                self.assertRedirects(
                    client.get(url, follow=True), redirect
                )

    def test_posts_templates(self):
        """Соответствие шаблонов и адресов приложения Post"""
        templates_cases = [
            [INDEX_URL, "posts/index.html", self.guest],
            [GROUP_URL, "posts/group_list.html", self.guest],
            [PROFILE_URL, "posts/profile.html", self.guest],
            [POST_CREATE_URL, "posts/create_post.html", self.authorized],
            [self.POST_DETAIL_URL, "posts/post_detail.html", self.guest],
            [self.POST_EDIT_URL, "posts/create_post.html", self.authorized],
            [FOLLOW_INDEX_URL, "posts/follow.html", self.authorized],
        ]
        for url, template, client in templates_cases:
            with self.subTest(url=url):
                self.assertTemplateUsed(client.get(url), template)

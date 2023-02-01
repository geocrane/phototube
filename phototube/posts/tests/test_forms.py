import os
import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .constants import (
    ANOTHER_SLUG,
    ANOTHER_USER,
    LOGIN_URL,
    NEW_SMALL_GIF,
    POST_CREATE_URL,
    PROFILE_URL,
    SMALL_GIF,
    TEST_USER,
    TEST_SLUG,
)

from ..models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
UPLOADED = SimpleUploadedFile(
    name="upload.gif", content=SMALL_GIF, content_type="image/small.gif"
)
UPLOAD_CREATE = SimpleUploadedFile(
    name="create.gif", content=SMALL_GIF, content_type="posts/small.gif"
)
UPLOAD_EDIT = SimpleUploadedFile(
    name="edit.gif", content=NEW_SMALL_GIF, content_type="posts/small.gif"
)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(TEST_USER)
        cls.not_author = User.objects.create_user(ANOTHER_USER)
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
        cls.post = Post.objects.create(
            text="Тестовый пост",
            author=cls.user,
            group=cls.group,
            image=UPLOADED,
        )
        cls.guest = Client()
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.POST_DETAIL_URL = reverse("posts:post_detail", args=[cls.post.id])
        cls.POST_EDIT_URL = reverse("posts:post_edit", args=[cls.post.id])
        cls.ADD_COMMENT_URL = reverse("posts:add_comment", args=[cls.post.id])
        cls.EDIT_LOGIN = f"{LOGIN_URL}?next={cls.POST_EDIT_URL}"

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_form_create_post(self):
        """Пост создается"""
        posts = set(Post.objects.all())
        post_data = {
            "text": "Текст формы",
            "group": self.group.id,
            "image": UPLOAD_CREATE,
        }
        response = self.authorized_client.post(
            POST_CREATE_URL,
            data=post_data,
            follow=True,
        )
        posts = set(Post.objects.all()) - posts
        self.assertEqual(len(posts), 1)
        post = posts.pop()
        self.assertEqual(post.text, post_data["text"])
        self.assertEqual(post.group.id, post_data["group"])
        self.assertEqual(post.author, self.user)
        self.assertEqual(
            os.path.basename(post.image.name), post_data["image"].name
        )
        self.assertEqual(post.image.size, post_data["image"].size)
        self.assertEqual(post.image.read(), post_data["image"].open().read())
        self.assertRedirects(response, PROFILE_URL)

    def test_author_can_edit_post(self):
        """Автор может редактировать пост"""
        post_data = {
            "text": "Измененный текст формы",
            "group": self.another_group.id,
            "image": UPLOAD_EDIT,
        }
        response = self.authorized_client.post(
            self.POST_EDIT_URL,
            data=post_data,
            follow=True,
        )
        post = response.context["post"]
        self.assertEqual(post.text, post_data["text"])
        self.assertEqual(post.group.id, post_data["group"])
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(
            os.path.basename(post.image.name), post_data["image"].name
        )
        self.assertEqual(post.image.size, post_data["image"].size)
        self.assertEqual(
            Image.open(post.image), Image.open(post_data["image"])
        )
        self.assertRedirects(response, self.POST_DETAIL_URL)

    def test_guest_and_notauthor_cant_edit_post(self):
        """Гость и неавтор не могут редактировать пост"""
        post_data = {
            "text": "Измененный текст формы",
            "group": self.another_group.id,
            "image": UPLOAD_EDIT,
        }
        clients = [self.guest, self.not_author_client]
        for client in clients:
            with self.subTest(client=client):
                self.client.post(
                    self.POST_EDIT_URL, data=post_data, follow=True
                )
                post = Post.objects.get(id=self.post.id)
                self.assertEqual(post.text, self.post.text)
                self.assertEqual(post.group, self.post.group)
                self.assertEqual(post.author, self.post.author)
                self.assertEqual(post.image, self.post.image)

    def test_form_create_comment(self):
        """Создается новый комментарий авторизованным пользователем"""
        comments = set(Comment.objects.all())
        comment_data = {"text": "Текст комментария"}
        self.authorized_client.post(
            self.ADD_COMMENT_URL,
            comment_data,
            follow=True,
        )
        comments = set(Comment.objects.all()) - comments
        self.assertEqual(len(comments), 1)
        comment = comments.pop()
        self.assertEqual(comment.text, comment_data["text"])
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)

    def test_create_edit_post_show_correct_context(self):
        """create_post и edit_post содержат форму создания поста"""
        urls = (POST_CREATE_URL, self.POST_EDIT_URL)
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get("form").fields.get(
                            value
                        )
                        self.assertIsInstance(form_field, expected)

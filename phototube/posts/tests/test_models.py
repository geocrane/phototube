from django.test import TestCase

from ..models import Comment, Follow, Group, Post, User
from .constants import ANOTHER_USER, TEST_USER, TEST_SLUG


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(TEST_USER)
        cls.follower = User.objects.create_user(ANOTHER_USER)
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug=TEST_SLUG,
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user, text="Тестовый текст", group=cls.group
        )
        cls.comment = Comment.objects.create(
            post=cls.post, text="Comment", author=cls.user
        )
        cls.following = Follow.objects.create(
            user=cls.user, author=cls.follower
        )

    def test_models_have_correct_object_names(self):
        """У моделей корректно работает __str__."""

        self.assertEqual(
            str(self.post),
            self.post.text[:Post.STR_POST_LENGTH],
        )
        self.assertEqual(str(self.group), self.group.title)
        self.assertEqual(
            str(self.comment), self.comment.text[:Comment.STR_COMMENT_LENGTH]
        )
        self.assertEqual(
            str(self.following),
            Follow.FOLLOW_STRING.format(
                user=self.user.username, author=self.follower.username
            ),
        )

    def test_post_verbose_name(self):
        """Доп. задание: verbose_name в модели Post совпадает с ожидаемым."""
        field_verboses = {
            "text": "Текст",
            "pub_date": "Дата создания",
            "author": "Автор",
            "group": "Группа",
        }
        for key, value in field_verboses.items():
            with self.subTest(field=key):
                self.assertEqual(Post._meta.get_field(key).verbose_name, value)

    def test_post_help_text(self):
        """Доп.задание: help_text в модели Post совпадает с ожидаемым."""
        field_help_texts = {
            "text": "Оставьте сообщение",
            "pub_date": "Дата создания",
            "author": "Автор поста",
            "group": "Группа, к которой относится пост",
        }
        for key, value in field_help_texts.items():
            with self.subTest(field=key):
                self.assertEqual(Post._meta.get_field(key).help_text, value)

    def test_group_verbose_name(self):
        """Доп. задание: verbose_name в модели Group совпадает с ожидаемым."""
        field_verboses = {
            "title": "Название",
            "slug": "Человекочитаемый идентификатор",
            "description": "Описание",
        }
        for key, value in field_verboses.items():
            with self.subTest(field=key):
                self.assertEqual(
                    Group._meta.get_field(key).verbose_name, value
                )

    def test_comment_verbose_name(self):
        """Доп.задание: verbose_name в модели Comment совпадает с ожидаемым."""
        field_verboses = {
            "post": "Комментарий",
            "author": "Автор",
            "text": "Текст",
        }
        for key, value in field_verboses.items():
            with self.subTest(field=key):
                self.assertEqual(
                    Comment._meta.get_field(key).verbose_name, value
                )

    def test_comment_help_text(self):
        """Доп.задание: help_text в модели Comment совпадает с ожидаемым."""
        field_help_texts = {
            "post": "Комментарий к посту",
            "author": "Автор комментария",
            "text": "Оставьте сообщение",
        }
        for key, value in field_help_texts.items():
            with self.subTest(field=key):
                self.assertEqual(Comment._meta.get_field(key).help_text, value)

    def test_follow_verbose_name(self):
        """Доп. задание: verbose_name в модели Follow совпадает с ожидаемым."""
        field_verboses = {
            "user": "Подписчик",
            "author": "Автор",
        }
        for key, value in field_verboses.items():
            with self.subTest(field=key):
                self.assertEqual(
                    Follow._meta.get_field(key).verbose_name, value
                )

    def test_follow_help_text(self):
        """Доп.задание: help_text в модели Follow совпадает с ожидаемым."""
        field_help_texts = {
            "user": "Подписчик на автора",
            "author": "Автор, на которого подписка",
        }
        for key, value in field_help_texts.items():
            with self.subTest(field=key):
                self.assertEqual(Follow._meta.get_field(key).help_text, value)

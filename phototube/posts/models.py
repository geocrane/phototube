from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(
        unique=True, verbose_name="slug"
    )
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.title


class Post(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
        help_text="Автор поста",
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Жанр",
        help_text="Выберите жанр фотографии",
    )
    image = models.ImageField("Фото", upload_to="posts/", blank=True)

    STR_POST_LENGTH = 10

    class Meta(CreatedModel.Meta):
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:self.STR_POST_LENGTH]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Комментарий",
        help_text="Оставьте комментарий к фотографии",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
        help_text="Автор комментария",
    )

    STR_COMMENT_LENGTH = 10

    class Meta(CreatedModel.Meta):
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:self.STR_COMMENT_LENGTH]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
        help_text="Подписчик на автора",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
        help_text="Автор, на которого подписка",
    )

    FOLLOW_STRING = "{user} подписан на {author}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_followers",
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name="no_self_following",
            ),
        ]

    def __str__(self):
        return self.FOLLOW_STRING.format(
            user=self.user.username, author=self.author.username
        )

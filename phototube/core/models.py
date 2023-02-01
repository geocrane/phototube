from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель"""
    text = models.TextField(
        verbose_name="Комментарий", help_text="Оставьте комментарий"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата создания",
    )

    class Meta:
        abstract = True
        ordering = ("-pub_date",)

import uuid

from django.db import models
from django.utils import timezone


class News(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        "Название",
        max_length=256,
    )
    description = models.TextField(
        "Описание",
        blank=True,
    )
    cover = models.ImageField(
        "Обложка",
        upload_to="images/news/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        "Дата",
        default=timezone.now,
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title}[{self.id}]"

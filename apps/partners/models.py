import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

FILE_EXTENSIONS = ("svg", "png", "jpg", "jpeg", "webp", "gif")


class Partners(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        "Название",
        max_length=256,
    )
    url = models.URLField(
        blank=True,
    )
    image = models.FileField(
        "Изображение",
        upload_to="images/partners/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=FILE_EXTENSIONS)],
    )

    class Meta:
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self) -> str:
        return f"{self.name}[{self.id}]"

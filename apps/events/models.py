import uuid

from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension
from django.db import models

from .enums import Precision
from .utils import (
    SLUG_MAX_LENGTH,
    DateRange,
    make_slug,
)


class Events(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(
        "Название",
        max_length=256,
    )
    slug = models.SlugField(
        "Короткая ссылка",
        max_length=SLUG_MAX_LENGTH,
        unique=True,
        blank=True,
        null=True,
        error_messages={
            "unique": "Мероприятие с такой ссылкой уже существует",
        },
    )
    description = models.CharField(
        "Описание",
        max_length=256,
        blank=True,
    )
    extended_description = models.TextField(
        "Развёрнутое описание",
        blank=True,
        help_text=(
            "Развёрнутое описание для подраздела "
            "«О мероприятии» на странице мероприятия"
        ),
    )
    place = models.CharField(
        "Место проведения",
        max_length=256,
        blank=True,
    )
    precision = models.CharField(
        "Точность",
        max_length=10,
        choices=Precision.choices,
        default=Precision.TIME,
    )
    start_datetime = models.DateTimeField(
        "Дата начала",
        help_text="Дата и время начала мероприятия",
    )
    end_datetime = models.DateTimeField(
        "Дата конца",
        blank=True,
        null=True,
        help_text="Дата и время конца мероприятия",
    )
    registration_link = models.URLField(
        "Ссылка на регистрацию",
        blank=True,
        null=True,
    )
    album_link = models.URLField(
        "Ссылка на альбом",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        super().clean()

        if not self.slug:
            self.slug = make_slug(self.title)

        errors = {}
        if not self.slug:
            errors["slug"] = "Не удалось составить ссылку из названия"

        if (
            self.start_datetime
            and self.end_datetime
            and self.end_datetime < self.start_datetime
        ):
            errors["end_datetime"] = "Дата завершения не может быть раньше даты начала"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def date_range_display(self) -> str:
        return DateRange(
            self.start_datetime,
            self.end_datetime,
            self.precision,
        ).range_display()


class EventImages(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    event = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Мероприятие",
    )
    image = models.ImageField(
        "Изображение",
        upload_to="images/events/",
        blank=True,
        null=True,
        validators=[validate_image_file_extension],
    )

    class Meta:
        verbose_name = "Изображение мероприятия"
        verbose_name_plural = "Изображения мероприятий"

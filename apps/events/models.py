import uuid

from django.core.exceptions import ValidationError
from django.db import models

from .enums import Precision
from .utils import (
    SLUG_MAX_LENGTH,
    DateRange,
    make_slug,
    period_end,
    truncate_date,
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
    finished_at = models.DateTimeField(
        "Конец периода с учётом точности",
        editable=False,
        db_index=True,
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
        self._truncate_dates()
        self._fill_slug()

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
        self._truncate_dates()
        self._fill_slug()
        self.finished_at = period_end(
            self.end_datetime or self.start_datetime,
            self.precision,
        )
        super().save(*args, **kwargs)

    @property
    def date_range_display(self) -> str:
        return DateRange(
            self.start_datetime,
            self.end_datetime,
            self.precision,
        ).range_display()

    def _truncate_dates(self) -> None:
        self.start_datetime = truncate_date(self.start_datetime, self.precision)
        self.end_datetime = truncate_date(self.end_datetime, self.precision)

    def _fill_slug(self) -> None:
        if not self.slug:
            self.slug = make_slug(self.title)


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
    )

    class Meta:
        verbose_name = "Изображение мероприятия"
        verbose_name_plural = "Изображения мероприятий"

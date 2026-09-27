import uuid

from django.db import models

from .enums import EventType, Precision
from .utils.date_utils import DateRange, parse_event_date


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
    description = models.CharField(
        "Описание",
        max_length=256,
        blank=True,
    )
    extended_description = models.TextField(
        "Развёрнутое описание",
        blank=True,
        help_text="Развёрнутое описание для подраздела \
            «О мероприятии» на странице мероприятия",
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
    type = models.CharField(
        "Тип мероприятия",
        max_length=10,
        choices=EventType.choices,
        default=EventType.FUTURE,
        help_text="Прошедшее или запланированное мероприятие",
    )
    start_datetime = models.CharField(
        "Дата начала",
        max_length=40,
        help_text="Дата начала мероприятия, например, 11.05.2006",
    )
    start_date = models.DateTimeField(
        "Дата начала",
        blank=True,
        null=True,
        editable=False,
        help_text=(
            "Заполняется автоматически из «Дата начала» при сохранении"
        ),
    )
    end_datetime = models.CharField(
        "Дата конца",
        max_length=40,
        blank=True,
        null=True,
        help_text="Дата конца мероприятия, например, 11.05.2006",
    )
    album_link = models.URLField(
        "Ссылка на альбом",
        blank=True,
        null=True,
    )
    registration_link = models.URLField(
        "Ссылка на регистрацию",
        blank=True,
        null=True,
    )

    @property
    def date_range_display(self):
        date_object = DateRange(
            self.start_datetime,
            self.end_datetime,
            self.precision,
        )
        return date_object.range_display()

    def save(self, *args, **kwargs) -> None:
        self.start_date = parse_event_date(self.start_datetime)
        super().save(*args, **kwargs)


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
    )
    image = models.ImageField(
        "Изображение",
        upload_to="images/events/",
        blank=True,
        null=True,
    )

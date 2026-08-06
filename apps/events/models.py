import uuid

from django.db import models
from django.db.models import CheckConstraint, Q

from .enums import Precision
from .utils import DateRange


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
    start_datetime = models.CharField(
        "Дата начала",
        max_length=40,
        help_text="Дата начала мероприятия, например, 11.05.2006",
    )
    end_datetime = models.CharField(
        "Дата конца",
        max_length=40,
        blank=True,
        null=True,
        help_text="Дата конца мероприятия, например, 11.05.2006",
    )

    @property
    def date_range_display(self):
        date_object = DateRange(
            self.start_datetime,
            self.end_datetime,
            self.precision,
        )
        return date_object.range_display()

    class Meta:
        abstract = True


class PastEvents(Events):
    album_link = models.URLField(
        "Ссылка на альбом",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Прошедшее мероприятие"
        verbose_name_plural = "Прошедшие мероприятия"


class FutureEvents(Events):
    registration_link = models.URLField(
        "Ссылка на регистрацию",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Запланированное мероприятие"
        verbose_name_plural = "Запланированные мероприятия"


class EventImages(models.Model):
    past_event = models.ForeignKey(
        PastEvents,
        on_delete=models.CASCADE,
        related_name="images",
        blank=True,
        null=True,
    )
    future_event = models.ForeignKey(
        FutureEvents,
        on_delete=models.CASCADE,
        related_name="images",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        "Изображение",
        upload_to="images/events/",
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            CheckConstraint(
                condition=(
                    Q(past_event__isnull=False, future_event__isnull=True)
                    | Q(past_event__isnull=True, future_event__isnull=False)
                ),
                name="only_one_event_link",
            )
        ]

import re
import uuid
from datetime import datetime

import msgspec
from django.db import migrations
from django.utils import timezone

PATTERNS: dict[str, re.Pattern[str]] = {
    "time": re.compile(
        r"^(?P<day>\d+)[/.-](?P<month>\d+)[/.-](?P<year>\d+)\s(?P<hour>\d+):(?P<minute>\d+)$"
    ),
    "day": re.compile(r"^(?P<day>\d+)[/.-](?P<month>\d+)[/.-](?P<year>\d+)$"),
    "month": re.compile(r"^(?P<month>\d+)[/.-](?P<year>\d+)$"),
    "year": re.compile(r"^(?P<year>\d+)$"),
}


class PrecisionError(Exception):
    """Ошибка некооректного значения перечисления Precision."""


class DateFormatError(ValueError):
    """Ошибка несоответствия строки формату или диапазонам значений."""


class DateStruct(msgspec.Struct):
    day: int = 1
    month: int = 1
    year: int = 2000
    hour: int = 0
    minute: int = 0


class Date:
    def __init__(self, str_date: str, precision: str):
        self.precision: str = precision
        self.data: DateStruct = self.processing(str_date.strip(), precision)

    @staticmethod
    def processing(str_date: str, precision: str) -> DateStruct:
        pattern = PATTERNS.get(precision)
        if pattern is None:
            raise PrecisionError(f"Неизвестный класс точности: {precision}")

        match = pattern.match(str_date)
        if not match:
            raise DateFormatError(
                f"Строка '{str_date}' не соответствует формату {precision}"
            )

        raw_values = match.groupdict()
        parsed: dict[str, int] = {k: int(v) for k, v in raw_values.items()}

        if "month" in parsed and not (1 <= parsed["month"] <= 12):
            raise DateFormatError(
                f"Месяц должен быть в диапазоне [1, 12]: {parsed['month']}"
            )
        if "hour" in parsed and not (0 <= parsed["hour"] <= 23):
            raise DateFormatError(
                f"Часы должны быть в диапазоне [0, 23]: {parsed['hour']}"
            )
        if "minute" in parsed and not (0 <= parsed["minute"] <= 59):
            raise DateFormatError(
                f"Минуты должны быть в диапазоне [0, 59]: {parsed['minute']}"
            )
        if "day" in parsed and parsed["day"] < 1:
            raise DateFormatError(
                f"День должен быть положительным числом: {parsed['day']}"
            )

        return DateStruct(**parsed)

    def to_datetime(self) -> datetime:
        return timezone.make_aware(
            datetime(
                year=self.data.year,
                month=self.data.month,
                day=self.data.day,
                hour=self.data.hour,
                minute=self.data.minute,
            )
        )


def copy_events(apps, schema_editor):
    FutureEvents = apps.get_model("events", "FutureEvents")
    PastEvents = apps.get_model("events", "PastEvents")
    Events = apps.get_model("events", "Events")
    EventImages = apps.get_model("events", "EventImages")

    used_ids = set()
    for Model, image_field, link_field in (
        (FutureEvents, "future_event_id", "registration_link"),
        (PastEvents, "past_event_id", "album_link"),
    ):
        for old in Model.objects.all():
            new_id = old.pk if old.pk not in used_ids else uuid.uuid4()
            used_ids.add(new_id)

            end_datetime = None
            if old.end_datetime:
                end_datetime = Date(old.end_datetime, old.precision).to_datetime()

            Events.objects.create(
                id=new_id,
                title=old.title,
                description=old.description,
                extended_description=old.extended_description,
                place=old.place,
                precision=old.precision,
                start_datetime=Date(old.start_datetime, old.precision).to_datetime(),
                end_datetime=end_datetime,
                **{link_field: getattr(old, link_field)},
            )
            EventImages.objects.filter(**{image_field: old.pk}).update(event_id=new_id)


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0004_events_unified"),
    ]

    operations = [
        migrations.RunPython(copy_events),
    ]

"""
Дата обрабатывается с учётом класса точности, задаваемого с помощью
перечисления Precision.

Обозначения:

- ``<day>`` - день, целое положительное число
- ``<month>`` - месяц, целое положительное число принадлежащее
множества ``{1, 2, ..., 12}``
- ``<year>`` - год, целое положительное число
- ``<Hour>`` - часы, целое неотрицательное число принадлежащее
множеству ``{0, 1, ..., 23}``
- ``<Minute>`` - минуты, целое неотрицательное число принадлежащее
множеству ``{0, 1, ..., 59}``
- ``<sep>`` - символ из множества {``/``, ``.``, ``-``}

Формат входных данных в зависимости от класса точности:

- Время (TIME)
    ``<day><sep><month><sep><year> <Hour>:<Minute>``

- День (DAY)
    ``<day><sep><month><sep><year>``

- Месяц (MONTH)
    ``<month><sep><year>``

- Год (YEAR)
    ``<year>``
"""

import re
from datetime import datetime

import msgspec
from django.utils import timezone

from apps.events.enums import Precision

from .exception.data_exception import DateFormatError, PrecisionError

MONTH_CASES = {
    "nomn": {
        1: "январь",
        2: "февраль",
        3: "март",
        4: "апрель",
        5: "май",
        6: "июнь",
        7: "июль",
        8: "август",
        9: "сентябрь",
        10: "октябрь",
        11: "ноябрь",
        12: "декабрь",
    },
    "gent": {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    },
}

FORMATS: dict[Precision, str] = {
    Precision.TIME: "%d.%m.%Y %H:%M",
    Precision.DAY: "%d.%m.%Y",
    Precision.MONTH: "%m.%Y",
    Precision.YEAR: "%Y",
}

PATTERNS: dict[Precision, re.Pattern[str]] = {
    Precision.TIME: re.compile(
        r"^(?P<day>\d+)[/.-](?P<month>\d+)[/.-](?P<year>\d+)\s(?P<hour>\d+):(?P<minute>\d+)$"
    ),
    Precision.DAY: re.compile(r"^(?P<day>\d+)[/.-](?P<month>\d+)[/.-](?P<year>\d+)$"),
    Precision.MONTH: re.compile(r"^(?P<month>\d+)[/.-](?P<year>\d+)$"),
    Precision.YEAR: re.compile(r"^(?P<year>\d+)$"),
}


class DateStruct(msgspec.Struct):
    day: int = 1
    month: int = 1
    year: int = 2000
    hour: int = 0
    minute: int = 0


class Date:
    def __init__(self, str_date: str, precision: Precision):
        self.precision: Precision = precision
        self.data: DateStruct = self.processing(str_date.strip(), precision)

    @staticmethod
    def processing(str_date: str, precision: Precision) -> DateStruct:
        pattern = PATTERNS.get(precision)
        if pattern is None:
            raise PrecisionError(f"Неизвестный класс точности: {precision}")

        match = pattern.match(str_date)
        if not match:
            raise DateFormatError(
                f"Строка '{str_date}' не соответствует формату {precision.name}"
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
        try:
            value = datetime(
                year=self.data.year,
                month=self.data.month,
                day=self.data.day,
                hour=self.data.hour,
                minute=self.data.minute,
            )
        except ValueError:
            raise DateFormatError(
                "Такой даты не существует: "
                f"{self.data.day:02}.{self.data.month:02}.{self.data.year}"
            ) from None
        return timezone.make_aware(value)


def format_date(date: datetime, precision: Precision) -> str:
    return timezone.localtime(date).strftime(FORMATS[precision])


class DateRange:
    def __init__(
        self, start: datetime, end: datetime | None, precision: Precision
    ) -> None:
        self.precision: Precision = precision
        self.start_date: datetime = timezone.localtime(start)
        self.end_date: datetime | None = end and timezone.localtime(end)

    def range_display(self) -> str:
        start_fmt = self._format_single_date(self.start_date)
        end_fmt = self._format_single_date(self.end_date)

        if end_fmt is None or end_fmt == start_fmt:
            return f"{start_fmt}"
        elif start_fmt is not None:
            if (
                self.precision == Precision.TIME
                and self.start_date.date() == self.end_date.date()
            ):
                day = self.start_date.day
                month = MONTH_CASES["gent"][self.start_date.month]
                year = self.start_date.year

                start_time = self.start_date.strftime("%H:%M")
                end_time = self.end_date.strftime("%H:%M")

                return f"{day} {month} {year} {start_time}-{end_time}"
            return f"{start_fmt} - {end_fmt}"
        else:
            return ""

    def _format_single_date(self, date: datetime | None) -> str | None:
        if not date:
            return None

        if self.precision == Precision.YEAR:
            return date.strftime("%Y")
        elif self.precision == Precision.MONTH:
            return f"{MONTH_CASES['nomn'][date.month]} {date.year}"
        elif self.precision == Precision.DAY:
            return f"{date.day} {MONTH_CASES['gent'][date.month]} {date.year}"
        elif self.precision == Precision.TIME:
            return (
                f"{date.day} {MONTH_CASES['gent'][date.month]} {date.year} "
                f"{date.strftime('%H:%M')}"
            )
        else:
            return str(date)

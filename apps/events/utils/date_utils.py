from datetime import datetime, timedelta

from django.utils import timezone

from apps.events.enums import Precision

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


def to_local(date: datetime | None) -> datetime | None:
    if date is None:
        return None

    if timezone.is_naive(date):
        return timezone.make_aware(date)
    return timezone.localtime(date)


def parse_date(date_str: str | None) -> datetime | None:
    """Разбирает дату в формате ISO 8601 и переводит её в локальное время."""
    if not date_str:
        return None

    try:
        return to_local(datetime.fromisoformat(date_str))
    except ValueError:
        raise ValueError(
            f"Не удалось распознать дату: {date_str}. "
            "Ожидается формат ISO 8601, например, 2006-11-05T18:30:00+03:00"
        ) from None


def truncate_date(date: datetime | None, precision: Precision) -> datetime | None:
    date = to_local(date)
    if date is None:
        return None

    if precision == Precision.YEAR:
        return date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif precision == Precision.MONTH:
        return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif precision == Precision.DAY:
        return date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif precision == Precision.TIME:
        return date.replace(second=0, microsecond=0)
    else:
        return date


def period_end(date: datetime | None, precision: Precision) -> datetime | None:
    date = truncate_date(date, precision)
    if date is None:
        return None

    if precision == Precision.YEAR:
        return date.replace(year=date.year + 1)
    elif precision == Precision.MONTH:
        if date.month == 12:
            return date.replace(year=date.year + 1, month=1)
        return date.replace(month=date.month + 1)
    elif precision == Precision.DAY:
        return date + timedelta(days=1)
    return date


class DateRange:
    def __init__(
        self, start: datetime, end: datetime | None, precision: Precision
    ) -> None:
        self.precision: Precision = precision
        self.start_date: datetime = to_local(start)
        self.end_date: datetime | None = to_local(end)

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

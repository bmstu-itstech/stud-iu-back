from enum import StrEnum

from django.db import models


class Precision(models.TextChoices):
    YEAR = "year", "Год"
    MONTH = "month", "Месяц"
    DAY = "day", "День"
    TIME = "time", "Время"


class EventSortField(StrEnum):
    STARTED_AT = "started_at"
    ENDED_AT = "ended_at"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"

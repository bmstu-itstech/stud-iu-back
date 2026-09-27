from django.db import models


class Precision(models.TextChoices):
    YEAR = "year", "Год"
    MONTH = "month", "Месяц"
    DAY = "day", "День"
    TIME = "time", "Время"


class EventType(models.TextChoices):
    PAST = "past", "Прошедшее"
    FUTURE = "future", "Запланированное"

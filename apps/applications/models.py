import uuid

from django.db import models


class Application(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    full_name = models.CharField("ФИО", max_length=256)
    group = models.CharField("Учебная группа", max_length=64)
    birth_date = models.DateField(
        "Дата рождения",
        blank=True,
        null=True,
    )
    telegram_url = models.URLField(
        "Ссылка на Telegram",
        blank=True,
        null=True,
    )
    vk_url = models.URLField(
        "Ссылка на профиль в vk",
        blank=True,
        null=True,
    )
    github_url = models.URLField(
        "Профиль на GitHub",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Анкета"
        verbose_name_plural = "Анкеты"

    def __str__(self) -> str:
        return f"{self.full_name} {self.group} [{self.id}]"

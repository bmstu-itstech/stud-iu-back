import uuid

from django.db import models


class Application(models.Model):
    class ActivityCategory(models.TextChoices):
        PROGRAMMING = (
            "programming",
            "Решение сложных технических задач, завязанных на программировании",
        )
        EVENT_PLANNING = (
            "event_planning",
            "Планирование и организация мероприятий",
        )
        CONTENT_CREATION = (
            "content_creation",
            "Создание визуального контента (СММ, Фото, Видео, Клипмейкинг, Графика, Дизайн)",
        )
        TEAM_BUILDING = (
            "team_building",
            "Работа с людьми и командообразование",
        )
        PARTNERSHIP = (
            "partnership",
            "Взаимодействие с партнерами, ведение деловых переговоров",
        )
        EVENT_TECH_SUPPORT = (
            "event_tech_support",
            "Поддержка и помощь в решении технических задач мероприятий (Настройка звука, модерация презентации, расстановка оборудования, т.д)",
        )

    class TechTask(models.TextChoices):
        WEB = "web", "Разработка сайтов"
        BOTS = "bots", "Разработка ботов"
        GAMES = "games", "Разработка игр"

    class VisualContentType(models.TextChoices):
        SMM = "smm", "СММ"
        PHOTO = "photo", "Фото"
        VIDEO = "video", "Видео"
        DESIGN = "design", "Дизайн"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField("ФИО", max_length=256)
    group = models.CharField("Учебная группа", max_length=64)
    birth_date = models.DateField("Дата рождения")
    telegram_url = models.URLField("Ссылка на Telegram")
    vk_url = models.URLField("Ссылка на VK")
    github_url = models.URLField("Профиль на GitHub", blank=True, null=True)
    portfolio_url = models.URLField(
        "Портфолио по работе с визуальным контентом",
        blank=True,
        null=True,
    )
    categories = models.JSONField(
        "Выбранные виды деятельности", default=list, blank=True
    )
    tech_tasks = models.JSONField("Технические задачи", default=list, blank=True)
    visual_content_types = models.JSONField(
        "Виды визуального контента", default=list, blank=True
    )

    class Meta:
        verbose_name = "Анкета"
        verbose_name_plural = "Анкеты"

    def __str__(self) -> str:
        return f"{self.full_name} {self.group} [{self.id}]"

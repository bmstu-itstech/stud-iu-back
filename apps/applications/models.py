import uuid

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

GROUP_PATTERN = (
    r"^((((ФМОП-)?(ИУ|ИБМ|МТ|СМ|БМТ|РЛ|Э|РК|ФН|Л|СГН|РКТ|АК|ПС|РТ|ЛТ|К|ЮР)(К)?[1-9]\d?)"
    r"|(ЮР(\.ДК)?))(К)?[ИЦ]?-(((1[0-2])|(\d))((\d)|(.\d\d+))([АМБ]?(В)?)))$"
)
PHONE_PATTERN = r"^\+7\d{10}$"
TELEGRAM_PATTERN = r"^@[A-Za-z0-9_]{3,32}$"
GITHUB_PATTERN = r"^https://github\.com/[A-Za-z0-9-]{1,39}/?$"


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
            "Создание визуального контента (СММ, Фото, Видео, Клипмейкинг, "
            "Графика, Дизайн)",
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
            "Поддержка и помощь в решении технических задач мероприятий ("
            "настройка звука, модерация презентации, расстановка оборудования, т.д)",
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
    group = models.CharField(
        "Учебная группа",
        max_length=64,
        validators=[RegexValidator(GROUP_PATTERN, "Неверный формат учебной группы")],
    )
    birth_date = models.DateField("Дата рождения")
    telegram = models.CharField(
        "Никнейм в Telegram",
        max_length=33,
        validators=[
            RegexValidator(TELEGRAM_PATTERN, "Никнейм должен быть в формате @username")
        ],
    )
    phone = models.CharField(
        "Контактный номер телефона",
        max_length=12,
        default="",
        validators=[
            RegexValidator(PHONE_PATTERN, "Телефон должен быть в формате +79991234567")
        ],
    )
    github_url = models.URLField(
        "Профиль на GitHub",
        blank=True,
        null=True,
        validators=[
            RegexValidator(GITHUB_PATTERN, "Ссылка должна вести на профиль GitHub")
        ],
    )
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

    def clean(self) -> None:
        super().clean()

        errors = {}
        for field, choices in (
            ("categories", self.ActivityCategory),
            ("tech_tasks", self.TechTask),
            ("visual_content_types", self.VisualContentType),
        ):
            unknown = set(getattr(self, field) or []) - set(choices.values)
            if unknown:
                errors[field] = f"Неизвестные значения: {', '.join(sorted(unknown))}"

        if errors:
            raise ValidationError(errors)

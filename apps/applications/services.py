from django.db.models import QuerySet

from apps.core.serializers import DatabaseId

from .models import Application
from .serializers import (
    ApplicationCreateSchema,
    ChoiceItemSchema,
    DependencySchema,
    FieldType,
    FormFieldSchema,
    OptionSchema,
)


class ApplicationNotFoundError(Exception):
    """Возвращает, когда сущность не найдена в базе данных."""


CATEGORY_MAP = dict(Application.ActivityCategory.choices)
TECH_TASK_MAP = dict(Application.TechTask.choices)
VISUAL_CONTENT_MAP = dict(Application.VisualContentType.choices)


def get_form_structure_service() -> list[FormFieldSchema]:
    """Возвращает структуру анкеты."""
    return [
        FormFieldSchema(
            key="full_name",
            label="ФИО",
            type=FieldType.TEXT,
            required=True,
        ),
        FormFieldSchema(
            key="group",
            label="Учебная группа",
            type=FieldType.TEXT,
            required=True,
        ),
        FormFieldSchema(
            key="birth_date",
            label="Дата рождения",
            type=FieldType.DATE,
            required=True,
        ),
        FormFieldSchema(
            key="telegram_url",
            label="Ссылка на Telegram",
            type=FieldType.URL,
            required=True,
        ),
        FormFieldSchema(
            key="vk_url",
            label="Ссылка на профиль в VK",
            type=FieldType.URL,
            required=True,
        ),
        FormFieldSchema(
            key="github_url",
            label="Профиль на GitHub",
            type=FieldType.URL,
            required=True,
            depends_on=DependencySchema(
                field="categories",
                contains=Application.ActivityCategory.PROGRAMMING.value,
            ),
        ),
        FormFieldSchema(
            key="portfolio_url",
            label="Ссылка на портфолио",
            type=FieldType.URL,
            required=False,
            depends_on=DependencySchema(
                field="categories",
                contains=Application.ActivityCategory.CONTENT_CREATION.value,
            ),
        ),
        FormFieldSchema(
            key="categories",
            label=("Какой из следующих видов деятельности вам наиболее интересен?"),
            type=FieldType.MULTIPLE_CHOICE,
            required=True,
            options=[
                OptionSchema(value=val, label=lbl)
                for val, lbl in Application.ActivityCategory.choices
            ],
        ),
        FormFieldSchema(
            key="tech_tasks",
            label="В решении каких технических задач вы заинтересованы?",
            type=FieldType.MULTIPLE_CHOICE,
            required=True,
            options=[
                OptionSchema(value=val, label=lbl)
                for val, lbl in Application.TechTask.choices
            ],
            depends_on=DependencySchema(
                field="categories",
                contains=Application.ActivityCategory.PROGRAMMING.value,
            ),
        ),
        FormFieldSchema(
            key="visual_content_types",
            label="Какой вид создания визуального контента вас интересует?",
            type=FieldType.MULTIPLE_CHOICE,
            required=True,
            options=[
                OptionSchema(value=val, label=lbl)
                for val, lbl in Application.VisualContentType.choices
            ],
            depends_on=DependencySchema(
                field="categories",
                contains=Application.ActivityCategory.CONTENT_CREATION.value,
            ),
        ),
    ]


def map_to_choice_items(
    values: list[str], label_map: dict[str, str]
) -> list[ChoiceItemSchema]:
    if not values:
        return []
    return [
        ChoiceItemSchema(value=val, label=label_map.get(val, val)) for val in values
    ]


def application_list_service() -> QuerySet[Application]:
    """Возвращает список всех сущностей Application."""
    return Application.objects.all()


def application_get_service(application_id: DatabaseId) -> Application:
    """Возвращает сущность Application по её ID.

    Если сущность не найдена, возникает ошибка ApplicationNotFoundError.
    """
    try:
        return Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        raise ApplicationNotFoundError from None


def application_create_service(payload: ApplicationCreateSchema) -> Application:
    """Создаёт новую сущность Application."""
    kwargs = {
        "full_name": payload.full_name,
        "group": payload.group,
        "birth_date": payload.birth_date,
        "telegram_url": payload.telegram_url,
        "vk_url": payload.vk_url,
        "github_url": payload.github_url,
        "portfolio_url": payload.portfolio_url,
        "categories": payload.categories,
        "tech_tasks": payload.tech_tasks,
        "visual_content_types": payload.visual_content_types,
    }

    return Application.objects.create(**kwargs)


def application_update_service(
    application_id: DatabaseId, payload: ApplicationCreateSchema
) -> Application:
    """Обновляет существующую сущность Application."""
    app = application_get_service(application_id)

    app.full_name = payload.full_name
    app.group = payload.group
    app.birth_date = payload.birth_date
    app.telegram_url = payload.telegram_url
    app.vk_url = payload.vk_url
    app.github_url = payload.github_url
    app.portfolio_url = payload.portfolio_url
    app.categories = payload.categories
    app.tech_tasks = payload.tech_tasks
    app.visual_content_types = payload.visual_content_types

    app.save()
    return app


def application_delete_service(application_id: DatabaseId) -> None:
    """Удаляет сущность BoardMember по её ID.

    Если сущность не найдена, возникает ошибка ApplicationNotFoundError.
    """
    deleted, _ = Application.objects.filter(pk=application_id).delete()
    if not deleted:
        raise ApplicationNotFoundError

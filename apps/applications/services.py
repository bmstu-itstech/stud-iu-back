from django.db.models import QuerySet

from apps.core.serializers import DatabaseId

from .models import Application
from .serializers import ApplicationCreateSchema


class ApplicationNotFoundError(Exception):
    """Возникает, когда сущность не найдена в базе данных."""


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
    }

    return Application.objects.create(**kwargs)


def application_update_service(
    application_id: DatabaseId, payload: ApplicationCreateSchema
) -> Application:
    """Обновляет существующую сущность Application.

    Если сущность не найдена, возникает ошибка ApplicationNotFoundError.
    """
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        raise ApplicationNotFoundError from None

    application.full_name = payload.full_name
    application.group = payload.group
    application.birth_date = payload.birth_date
    application.telegram_url = payload.telegram_url
    application.vk_url = payload.vk_url
    application.github_url = payload.github_url

    application.save()
    return application


def application_delete_service(application_id: DatabaseId) -> None:
    """Удаляет сущность Application по её ID.

    Если сущность не найдена, возникает ошибка ApplicationNotFoundError.
    """
    deleted, _ = Application.objects.filter(pk=application_id).delete()
    if not deleted:
        raise ApplicationNotFoundError

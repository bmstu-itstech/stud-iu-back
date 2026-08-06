from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet

from apps.core.serializers import DatabaseId

from .models import News
from .serializers import NewsCreateSchema


class NewsNotFoundError(Exception):
    """Возникает, когда сущность не найден в базе данных."""


def news_list_service() -> QuerySet[News]:
    """Возвращает список всех сущностей News."""
    return News.objects.all()


def news_get_service(news_id: DatabaseId) -> News:
    """Возвращает сущность News по её ID.

    Если сущность не найдена, возникает ошибка NewsNotFoundError.
    """
    try:
        return News.objects.get(pk=news_id)
    except News.DoesNotExist:
        raise NewsNotFoundError from None


def news_create_service(
    payload: NewsCreateSchema,
    cover: UploadedFile | None = None,
) -> News:
    """Создаёт новую сущность News."""
    kwargs = {
        "title": payload.title,
        "description": payload.description,
    }

    if payload.created_at is not None:
        kwargs["created_at"] = payload.created_at

    if cover is not None:
        kwargs["cover"] = cover

    return News.objects.create(**kwargs)


def news_update_service(
    news_id: DatabaseId, payload: NewsCreateSchema, cover: UploadedFile | None = None
) -> News:
    """Обновляет существующую сущность News.

    Если сущность не найдена, возникает ошибка NewsNotFoundError.
    """
    try:
        news = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        raise NewsNotFoundError from None

    news.title = payload.title
    news.description = payload.description

    if payload.created_at is not None:
        news.created_at = payload.created_at

    if cover is not None:
        news.cover = cover

    news.save()
    return news


def news_delete_service(news_id: DatabaseId) -> None:
    """Удаляет сущность News по её ID.

    Если сущность не найдена, возникает ошибка NewsNotFoundError.
    """
    deleted, _ = News.objects.filter(pk=news_id).delete()
    if not deleted:
        raise NewsNotFoundError

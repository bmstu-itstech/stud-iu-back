import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.db.models import Case, F, Q, QuerySet, When
from django.db.models.functions import Coalesce
from django.utils import timezone

from apps.events.enums import EventPeriod, EventSortField, Precision, SortOrder
from apps.events.models import EventImages, Events
from apps.events.serializers import EventCreateSchema
from apps.events.utils import Date, DateFormatError

from .exceptions import EventNotFoundError


def event_list_service(
    period: EventPeriod | None = None,
    sort: EventSortField = EventSortField.STARTED_AT,
    order: SortOrder | None = None,
) -> QuerySet[Events]:
    """Возвращает мероприятия за период, отсортированные по дате.

    По умолчанию прошедшие идут от новых к старым, будущие - от ближайших.
    Без периода сначала идут будущие от ближайших, затем прошедшие от новых.
    """
    events = Events.objects.prefetch_related("images").alias(
        ended_at=Coalesce("end_datetime", "start_datetime"),
    )

    now = timezone.now()
    if period == EventPeriod.PAST:
        events = events.filter(ended_at__lt=now)
    elif period == EventPeriod.FUTURE:
        events = events.filter(ended_at__gte=now)

    field = F("ended_at" if sort == EventSortField.ENDED_AT else "start_datetime")

    if period is None and order is None:
        upcoming = Q(ended_at__gte=now)
        return events.order_by(
            Case(When(upcoming, then=0), default=1),
            Case(When(upcoming, then=field)).asc(),
            Case(When(~upcoming, then=field)).desc(),
            "pk",
        )

    if order is None:
        order = SortOrder.DESC if period == EventPeriod.PAST else SortOrder.ASC

    return events.order_by(
        field.desc() if order == SortOrder.DESC else field.asc(),
        "pk",
    )


def event_get_service(event_ref: str) -> Events:
    """Возвращает мероприятие.

    Если мероприятие не найдено, возникает ошибка EventNotFoundError.
    """
    return _get_event(event_ref, Events.objects.prefetch_related("images"))


@transaction.atomic
def event_create_service(
    payload: EventCreateSchema, images: list[UploadedFile] | None = None
) -> Events:
    """Создаёт мероприятие."""
    event = Events()
    _fill_event_fields(event, payload)

    if images:
        _create_event_images(event, images)

    return event


@transaction.atomic
def event_update_service(
    event_ref: str,
    payload: EventCreateSchema,
    images: list[UploadedFile] | None = None,
) -> Events:
    """Обновляет мероприятие.

    Если мероприятие не найдено, возникает ошибка EventNotFoundError.
    """
    event = _get_event(event_ref, Events.objects.all())

    _fill_event_fields(event, payload)

    if images is not None:
        event.images.all().delete()
        _create_event_images(event, images)

    return event


def event_delete_service(event_ref: str) -> None:
    """Удаляет мероприятие.

    Если мероприятие не найдено, возникает ошибка EventNotFoundError.
    """
    _get_event(event_ref, Events.objects.all()).delete()


def _get_event(event_ref: str, events: QuerySet[Events]) -> Events:
    """Поиск мероприятия."""
    try:
        return events.get(slug=event_ref)
    except Events.DoesNotExist:
        pass

    try:
        return events.get(pk=uuid.UUID(event_ref))
    except ValueError, Events.DoesNotExist:
        raise EventNotFoundError from None


def _fill_event_fields(event: Events, payload: EventCreateSchema) -> None:
    event.title = payload.title
    if payload.slug is not None:
        event.slug = payload.slug
    event.description = payload.description
    event.extended_description = payload.extended_description
    event.place = payload.place
    event.precision = _parse_precision(payload.precision)
    event.start_datetime = _parse_date(
        "start_datetime", payload.start_datetime, event.precision
    )
    event.end_datetime = _parse_date(
        "end_datetime", payload.end_datetime, event.precision
    )
    event.album_link = payload.album_link
    event.registration_link = payload.registration_link

    event.save()


def _parse_precision(value: str) -> Precision:
    try:
        return Precision(value)
    except ValueError:
        raise ValidationError(
            {"precision": f"Неизвестный класс точности: {value}"}
        ) from None


def _parse_date(field: str, value: str | None, precision: Precision) -> datetime | None:
    if value is None:
        return None
    try:
        return Date(value, precision).to_datetime()
    except DateFormatError as exc:
        raise ValidationError({field: str(exc)}) from None


def _create_event_images(event: Events, images: list[UploadedFile]) -> None:
    for image in images:
        event_image = EventImages(event=event, image=image)
        event_image.full_clean()
        event_image.save()

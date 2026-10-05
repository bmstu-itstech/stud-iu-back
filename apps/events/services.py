import uuid

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.db.models import F, QuerySet
from django.db.models.functions import Coalesce
from django.utils import timezone

from apps.events.enums import EventPeriod, EventSortField, SortOrder
from apps.events.models import EventImages, Events
from apps.events.serializers import EventCreateSchema
from apps.events.utils import parse_date

from .exceptions import EventNotFoundError


def event_list_service(
    period: EventPeriod | None = None,
    sort: EventSortField = EventSortField.STARTED_AT,
    order: SortOrder | None = None,
) -> QuerySet[Events]:
    """Возвращает мероприятия за период, отсортированные по дате.

    По умолчанию прошедшие идут от новых к старым, остальные - от ближайших.
    """
    events = Events.objects.prefetch_related("images").annotate(
        ended_at=Coalesce("end_datetime", "start_datetime"),
    )

    now = timezone.now()
    if period == EventPeriod.PAST:
        events = events.filter(finished_at__lt=now)
    elif period == EventPeriod.FUTURE:
        events = events.filter(finished_at__gte=now)

    if order is None:
        order = SortOrder.DESC if period == EventPeriod.PAST else SortOrder.ASC

    field = F("ended_at" if sort == EventSortField.ENDED_AT else "start_datetime")
    return events.order_by(
        field.desc() if order == SortOrder.DESC else field.asc(),
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
    if images:
        _validate_event_images(images)

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

    if images:
        _validate_event_images(images)

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


def _validate_event_images(images: list[UploadedFile]) -> None:
    image_field = forms.ImageField()
    for image in images:
        try:
            image_field.clean(image)
        except ValidationError as exc:
            raise ValidationError(
                {"images": f"{image.name}: {exc.messages[0]}"}
            ) from None


def _fill_event_fields(event: Events, payload: EventCreateSchema) -> None:
    dates = _parse_event_dates(payload)

    event.title = payload.title
    if payload.slug is not None:
        event.slug = payload.slug
    event.description = payload.description
    event.extended_description = payload.extended_description
    event.place = payload.place
    event.precision = payload.precision
    event.start_datetime = dates["start_datetime"]
    event.end_datetime = dates["end_datetime"]
    event.album_link = payload.album_link
    event.registration_link = payload.registration_link
    event.full_clean()
    event.save()


def _parse_event_dates(payload: EventCreateSchema) -> dict:
    dates = {}
    errors = {}
    for field in ("start_datetime", "end_datetime"):
        try:
            dates[field] = parse_date(getattr(payload, field), payload.precision)
        except ValueError as exc:
            errors[field] = str(exc)

    if errors:
        raise ValidationError(errors)
    return dates


def _create_event_images(event: Events, images: list[UploadedFile]) -> None:
    for image in images:
        EventImages.objects.create(event=event, image=image)

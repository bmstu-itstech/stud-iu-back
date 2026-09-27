from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.db.models import F, QuerySet

from apps.core.serializers import DatabaseId
from apps.events.enums import EventType
from apps.events.models import EventImages, Events
from apps.events.serializers import EventCreateSchema

from .exceptions import EventNotFoundError


def events_list_service(event_type: str) -> QuerySet[Events]:
    start_order = (
        F("start_date").desc(nulls_last=True)
        if event_type == EventType.PAST
        else F("start_date").asc(nulls_last=True)
    )
    return Events.objects.filter(type=event_type).prefetch_related(
        "images"
    ).order_by(start_order)


def event_get_service(event_id: DatabaseId) -> Events:
    try:
        return Events.objects.prefetch_related("images").get(pk=event_id)
    except Events.DoesNotExist:
        raise EventNotFoundError from None


def _create_event_images(event: Events, images: list[UploadedFile]) -> None:
    for image in images:
        EventImages.objects.create(event=event, image=image)


@transaction.atomic
def event_create_service(
    payload: EventCreateSchema, images: list[UploadedFile] | None = None
) -> Events:
    event = Events.objects.create(
        title=payload.title,
        description=payload.description,
        extended_description=payload.extended_description,
        place=payload.place,
        precision=payload.precision,
        type=payload.type,
        start_datetime=payload.start_datetime,
        end_datetime=payload.end_datetime,
        album_link=payload.album_link,
        registration_link=payload.registration_link,
    )
    if images:
        _create_event_images(event, images)

    return event


def _update_event_fields(event: Events, payload: EventCreateSchema) -> None:
    event.title = payload.title
    event.description = payload.description
    event.extended_description = payload.extended_description
    event.place = payload.place
    event.precision = payload.precision
    event.type = payload.type
    event.start_datetime = payload.start_datetime
    event.end_datetime = payload.end_datetime
    event.album_link = payload.album_link
    event.registration_link = payload.registration_link
    event.save()


def _replace_event_images(event: Events, images: list[UploadedFile]) -> None:
    event.images.all().delete()
    _create_event_images(event, images)


@transaction.atomic
def event_update_service(
    event_id: DatabaseId,
    payload: EventCreateSchema,
    images: list[UploadedFile] | None = None,
) -> Events:
    try:
        event = Events.objects.get(pk=event_id)
    except Events.DoesNotExist:
        raise EventNotFoundError from None

    _update_event_fields(event, payload)

    if images is not None:
        _replace_event_images(event, images)

    return event


def event_delete_service(event_id: DatabaseId) -> None:
    deleted, _ = Events.objects.filter(pk=event_id).delete()
    if not deleted:
        raise EventNotFoundError

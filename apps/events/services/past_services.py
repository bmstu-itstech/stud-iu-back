from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.db.models import QuerySet

from apps.core.serializers import DatabaseId
from apps.events.models import EventImages, PastEvents
from apps.events.serializers import PastEventCreateSchema

from .exceptions import EventNotFoundError


def past_event_list_service() -> QuerySet[PastEvents]:
    return PastEvents.objects.prefetch_related("images").all()


def past_event_get_service(event_id: DatabaseId) -> PastEvents:
    try:
        return PastEvents.objects.prefetch_related("images").get(pk=event_id)
    except PastEvents.DoesNotExist:
        raise EventNotFoundError from None


def _create_past_event_images(event: PastEvents, images: list[UploadedFile]) -> None:
    for image in images:
        EventImages.objects.create(past_event=event, image=image)


@transaction.atomic
def past_event_create_service(
    payload: PastEventCreateSchema, images: list[UploadedFile] | None = None
) -> PastEvents:
    event = PastEvents.objects.create(
        title=payload.title,
        description=payload.description,
        extended_description=payload.extended_description,
        place=payload.place,
        precision=payload.precision,
        start_datetime=payload.start_datetime,
        end_datetime=payload.end_datetime,
        album_link=payload.album_link,
    )
    if images:
        _create_past_event_images(event, images)

    return event


def _update_past_event_fields(
    event: PastEvents, payload: PastEventCreateSchema
) -> None:
    event.title = payload.title
    event.description = payload.description
    event.extended_description = payload.extended_description
    event.place = payload.place
    event.precision = payload.precision
    event.start_datetime = payload.start_datetime
    event.end_datetime = payload.end_datetime
    event.album_link = payload.album_link
    event.save()


def _replace_past_event_images(event: PastEvents, images: list[UploadedFile]) -> None:
    event.images.all().delete()
    _create_past_event_images(event, images)


@transaction.atomic
def past_event_update_service(
    event_id: DatabaseId,
    payload: PastEventCreateSchema,
    images: list[UploadedFile] | None = None,
) -> PastEvents:
    try:
        event = PastEvents.objects.get(pk=event_id)
    except PastEvents.DoesNotExist:
        raise EventNotFoundError from None

    _update_past_event_fields(event, payload)

    if images is not None:
        _replace_past_event_images(event, images)

    return event


def past_event_delete_service(event_id: DatabaseId) -> None:
    deleted, _ = PastEvents.objects.filter(pk=event_id).delete()
    if not deleted:
        raise EventNotFoundError

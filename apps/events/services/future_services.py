from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.db.models import QuerySet

from apps.core.serializers import DatabaseId
from apps.events.models import EventImages, FutureEvents
from apps.events.serializers import FutureEventCreateSchema

from .exceptions import EventNotFoundError


def future_event_list_service() -> QuerySet[FutureEvents]:
    return FutureEvents.objects.prefetch_related("images").all()


def future_event_get_service(event_id: DatabaseId) -> FutureEvents:
    try:
        return FutureEvents.objects.prefetch_related("images").get(pk=event_id)
    except FutureEvents.DoesNotExist:
        raise EventNotFoundError from None


def _create_future_event_images(
    event: FutureEvents, images: list[UploadedFile]
) -> None:
    for image in images:
        EventImages.objects.create(future_event=event, image=image)


@transaction.atomic
def future_event_create_service(
    payload: FutureEventCreateSchema, images: list[UploadedFile] | None = None
) -> FutureEvents:
    event = FutureEvents.objects.create(
        title=payload.title,
        description=payload.description,
        extended_description=payload.extended_description,
        place=payload.place,
        precision=payload.precision,
        start_datetime=payload.start_datetime,
        end_datetime=payload.end_datetime,
        registration_link=payload.registration_link,
    )
    if images:
        _create_future_event_images(event, images)

    return event


def _update_future_event_fields(
    event: FutureEvents, payload: FutureEventCreateSchema
) -> None:
    event.title = payload.title
    event.description = payload.description
    event.extended_description = payload.extended_description
    event.place = payload.place
    event.precision = payload.precision
    event.start_datetime = payload.start_datetime
    event.end_datetime = payload.end_datetime
    event.registration_link = payload.registration_link
    event.save()


def _replace_future_event_images(
    event: FutureEvents, images: list[UploadedFile]
) -> None:
    event.images.all().delete()
    _create_future_event_images(event, images)


@transaction.atomic
def future_event_update_service(
    event_id: DatabaseId,
    payload: FutureEventCreateSchema,
    images: list[UploadedFile] | None = None,
) -> FutureEvents:
    try:
        event = FutureEvents.objects.get(pk=event_id)
    except FutureEvents.DoesNotExist:
        raise EventNotFoundError from None

    _update_future_event_fields(event, payload)

    if images is not None:
        _replace_future_event_images(event, images)

    return event


def future_event_delete_service(event_id: DatabaseId) -> None:
    deleted, _ = FutureEvents.objects.filter(pk=event_id).delete()
    if not deleted:
        raise EventNotFoundError

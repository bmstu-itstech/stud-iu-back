from http import HTTPStatus
from typing import final, override

from django.http import HttpResponse
from dmr import Body, Controller, Path, modify
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.metadata import ResponseSpec
from dmr.parsers import MultiPartParser
from dmr.plugins.msgspec import MsgspecJsonParser, MsgspecSerializer

from apps.events.enums import EventType
from apps.events.serializers import EventCreateSchema, EventPathSchema, EventSchema
from apps.events.services import (
    EventNotFoundError,
    event_create_service,
    event_delete_service,
    event_get_service,
    event_update_service,
    events_list_service,
)

from .base import _images_to_schema


def _event_to_schema(event) -> EventSchema:
    return EventSchema(
        id=str(event.pk),
        title=event.title,
        description=event.description,
        extended_description=event.extended_description,
        place=event.place,
        precision=event.precision,
        type=event.type,
        start_datetime=event.start_datetime,
        end_datetime=event.end_datetime,
        date_range_display=event.date_range_display,
        album_link=event.album_link,
        registration_link=event.registration_link,
        images=_images_to_schema(event),
    )


@final
class EventsListController(Controller[MsgspecSerializer]):

    parsers = (
        MsgspecJsonParser(),
        MultiPartParser(),
    )

    def get(self) -> list[EventSchema]:
        return [
            _event_to_schema(event)
            for event in events_list_service(EventType.FUTURE)
        ]

    def post(self, parsed_body: Body[EventCreateSchema]) -> EventSchema:
        images = self.request.FILES.getlist("images") or None
        event = event_create_service(parsed_body, images=images)
        return _event_to_schema(event)


@final
class PastEventsListController(Controller[MsgspecSerializer]):

    parsers = (
        MsgspecJsonParser(),
        MultiPartParser(),
    )

    def get(self) -> list[EventSchema]:
        return [
            _event_to_schema(event)
            for event in events_list_service(EventType.PAST)
        ]

    def post(self, parsed_body: Body[EventCreateSchema]) -> EventSchema:
        parsed_body.type = EventType.PAST
        images = self.request.FILES.getlist("images") or None
        event = event_create_service(parsed_body, images=images)
        return _event_to_schema(event)


@final
class EventDetailController(Controller[MsgspecSerializer]):

    parsers = (
        MsgspecJsonParser(),
        MultiPartParser(),
    )

    responses = (
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.NOT_FOUND,
        ),
    )

    def get(self, parsed_path: Path[EventPathSchema]) -> EventSchema:
        return _event_to_schema(event_get_service(parsed_path.event_id))

    def put(
        self,
        parsed_path: Path[EventPathSchema],
        parsed_body: Body[EventCreateSchema],
    ) -> EventSchema:
        images = (
            self.request.FILES.getlist("images")
            if "images" in self.request.FILES
            else None
        )
        event = event_update_service(
            parsed_path.event_id, parsed_body, images=images
        )
        return _event_to_schema(event)

    @modify(status_code=HTTPStatus.NO_CONTENT)
    def delete(self, parsed_path: Path[EventPathSchema]) -> None:
        event_delete_service(parsed_path.event_id)

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, EventNotFoundError):
            return self.to_error(
                self.format_error("Event not found", error_type=ErrorType.value_error),
                status_code=HTTPStatus.NOT_FOUND,
            )
        return super().handle_error(endpoint, controller, exc)

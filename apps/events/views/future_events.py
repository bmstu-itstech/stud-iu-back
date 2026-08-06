from http import HTTPStatus
from typing import final, override

from django.http import HttpResponse
from dmr import Body, Controller, Path, modify
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.plugins.msgspec import MsgspecSerializer

from apps.events.serializers import (
    EventPathSchema,
    FutureEventCreateSchema,
    FutureEventSchema,
)
from apps.events.services import (
    EventNotFoundError,
    future_event_create_service,
    future_event_delete_service,
    future_event_get_service,
    future_event_list_service,
    future_event_update_service,
)

from .base import _images_to_schema


def _future_to_schema(event) -> FutureEventSchema:
    return FutureEventSchema(
        id=str(event.pk),
        title=event.title,
        description=event.description,
        place=event.place,
        precision=event.precision,
        date_range_display=event.date_range_display,
        registration_link=event.registration_link,
        images=_images_to_schema(event),
    )


@final
class FutureEventListController(Controller[MsgspecSerializer]):
    def get(self) -> list[FutureEventSchema]:
        return [_future_to_schema(e) for e in future_event_list_service()]

    def post(self, parsed_body: Body[FutureEventCreateSchema]) -> FutureEventSchema:
        images = self.request.FILES.getlist("images") or None
        event = future_event_create_service(parsed_body, images=images)
        return _future_to_schema(event)


@final
class FutureEventDetailController(Controller[MsgspecSerializer]):
    def get(self, parsed_path: Path[EventPathSchema]) -> FutureEventSchema:
        return _future_to_schema(future_event_get_service(parsed_path.event_id))

    def put(
        self,
        parsed_path: Path[EventPathSchema],
        parsed_body: Body[FutureEventCreateSchema],
    ) -> FutureEventSchema:
        images = (
            self.request.FILES.getlist("images")
            if "images" in self.request.FILES
            else None
        )
        event = future_event_update_service(
            parsed_path.event_id, parsed_body, images=images
        )
        return _future_to_schema(event)

    @modify(status_code=HTTPStatus.NO_CONTENT)
    def delete(self, parsed_path: Path[EventPathSchema]) -> None:
        future_event_delete_service(parsed_path.event_id)

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

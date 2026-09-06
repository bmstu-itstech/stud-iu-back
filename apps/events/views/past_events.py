from http import HTTPStatus
from typing import final, override

from django.http import HttpResponse
from dmr import Body, Controller, Path, modify
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.metadata import ResponseSpec
from dmr.parsers import MultiPartParser
from dmr.plugins.msgspec import MsgspecJsonParser, MsgspecSerializer

from apps.events.serializers import (
    EventPathSchema,
    PastEventCreateSchema,
    PastEventSchema,
)
from apps.events.services import (
    EventNotFoundError,
    past_event_create_service,
    past_event_delete_service,
    past_event_get_service,
    past_event_list_service,
    past_event_update_service,
)

from .base import _images_to_schema


def _past_to_schema(event) -> PastEventSchema:
    return PastEventSchema(
        id=str(event.pk),
        title=event.title,
        description=event.description,
        extended_description=event.extended_description,
        place=event.place,
        precision=event.precision,
        start_datetime=event.start_datetime,
        end_datetime=event.end_datetime,
        date_range_display=event.date_range_display,
        album_link=event.album_link,
        images=_images_to_schema(event),
    )


@final
class PastEventListController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с коллекцией сущностей PastEvent."""

    parsers = (
        MsgspecJsonParser(),
        MultiPartParser(),
    )

    def get(self) -> list[PastEventSchema]:
        """Получение списка всех сущностей PastEvent."""
        return [_past_to_schema(e) for e in past_event_list_service()]

    def post(self, parsed_body: Body[PastEventCreateSchema]) -> PastEventSchema:
        """Создание новой сущности PastEvent."""
        images = self.request.FILES.getlist("images") or None
        event = past_event_create_service(parsed_body, images=images)
        return _past_to_schema(event)


@final
class PastEventDetailController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с сущностью PastEvent."""

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

    def get(self, parsed_path: Path[EventPathSchema]) -> PastEventSchema:
        """Получение сущности PastEvent по её ID."""
        return _past_to_schema(past_event_get_service(parsed_path.event_id))

    def put(
        self,
        parsed_path: Path[EventPathSchema],
        parsed_body: Body[PastEventCreateSchema],
    ) -> PastEventSchema:
        """Обновление существующей сущности PastEvent по её ID."""
        images = (
            self.request.FILES.getlist("images")
            if "images" in self.request.FILES
            else None
        )
        event = past_event_update_service(
            parsed_path.event_id, parsed_body, images=images
        )
        return _past_to_schema(event)

    @modify(status_code=HTTPStatus.NO_CONTENT)
    def delete(self, parsed_path: Path[EventPathSchema]) -> None:
        """Удаление сущности PastEvent по её ID."""
        past_event_delete_service(parsed_path.event_id)

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

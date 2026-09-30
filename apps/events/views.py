from http import HTTPStatus
from typing import final, override

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from dmr import Body, Controller, Path, Query, modify
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.metadata import ResponseSpec
from dmr.parsers import MultiPartParser
from dmr.plugins.msgspec import MsgspecJsonParser, MsgspecSerializer

from .models import Events
from .serializers import (
    EventCreateSchema,
    EventImageSchema,
    EventListQuerySchema,
    EventPathSchema,
    EventSchema,
)
from .services import (
    EventNotFoundError,
    event_create_service,
    event_delete_service,
    event_get_service,
    event_list_service,
    event_update_service,
)
from .utils import to_local


def _to_schema(event: Events) -> EventSchema:
    return EventSchema(
        id=event.pk,
        title=event.title,
        description=event.description,
        extended_description=event.extended_description,
        place=event.place,
        precision=event.precision,
        start_datetime=to_local(event.start_datetime),
        end_datetime=to_local(event.end_datetime),
        date_range_display=event.date_range_display,
        images=[
            EventImageSchema(
                id=image.pk,
                image=image.image.url if image.image else None,
            )
            for image in event.images.all()
        ],
        album_link=event.album_link,
        registration_link=event.registration_link,
    )


def _validation_error(controller: Controller, exc: ValidationError) -> HttpResponse:
    detail = [
        {"msg": messages[0], "loc": [field], "type": ErrorType.value_error}
        for field, messages in exc.message_dict.items()
    ]
    return controller.to_error(
        {"detail": detail},
        status_code=HTTPStatus.BAD_REQUEST,
    )


@final
class EventListController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с коллекцией сущностей Event."""

    parsers = (
        MsgspecJsonParser(),
        MultiPartParser(),
    )

    responses = (
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.BAD_REQUEST,
        ),
    )

    def get(self, parsed_query: Query[EventListQuerySchema]) -> list[EventSchema]:
        """Получение списка сущностей Event.

        Фильтр: `period=past|future`.
        Сортировка: `sort=started_at|ended_at`, `order=asc|desc`.
        """
        events = event_list_service(
            period=parsed_query.period,
            sort=parsed_query.sort,
            order=parsed_query.order,
        )
        return [_to_schema(event) for event in events]

    def post(self, parsed_body: Body[EventCreateSchema]) -> EventSchema:
        """Создание новой сущности Event."""
        images = self.request.FILES.getlist("images") or None
        return _to_schema(event_create_service(parsed_body, images=images))

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, ValidationError):
            return _validation_error(self, exc)
        return super().handle_error(endpoint, controller, exc)


@final
class EventDetailController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с сущностью Event."""

    parsers = (
        MsgspecJsonParser(),
        MultiPartParser(),
    )

    responses = (
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.NOT_FOUND,
        ),
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.BAD_REQUEST,
        ),
    )

    def get(self, parsed_path: Path[EventPathSchema]) -> EventSchema:
        """Получение сущности Event по её ID."""
        return _to_schema(event_get_service(parsed_path.event_id))

    def put(
        self,
        parsed_path: Path[EventPathSchema],
        parsed_body: Body[EventCreateSchema],
    ) -> EventSchema:
        """Обновление существующей сущности Event по её ID."""
        images = (
            self.request.FILES.getlist("images")
            if "images" in self.request.FILES
            else None
        )
        return _to_schema(
            event_update_service(parsed_path.event_id, parsed_body, images=images)
        )

    @modify(status_code=HTTPStatus.NO_CONTENT)
    def delete(self, parsed_path: Path[EventPathSchema]) -> None:
        """Удаление сущности Event по её ID."""
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
                self.format_error(
                    "Event not found",
                    error_type=ErrorType.value_error,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )
        if isinstance(exc, ValidationError):
            return _validation_error(self, exc)
        return super().handle_error(endpoint, controller, exc)

from http import HTTPStatus
from typing import final, override

from django.http import HttpResponse
from dmr import Body, Controller, Path, modify
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.metadata import ResponseSpec
from dmr.plugins.msgspec import MsgspecSerializer

from .models import Application
from .serializers import (
    ApplicationCreateSchema,
    ApplicationPathSchema,
    ApplicationSchema,
)
from .services import (
    ApplicationNotFoundError,
    application_create_service,
    application_delete_service,
    application_get_service,
    application_list_service,
    application_update_service,
)


def _to_schema(application: Application) -> ApplicationSchema:
    return ApplicationSchema(
        full_name=application.full_name,
        group=application.group,
        birth_date=application.birth_date,
        telegram_url=application.telegram_url,
        vk_url=application.vk_url,
        github_url=application.github_url,
    )


@final
class ApplicationController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с коллекцией сущностей Application."""

    def get(self) -> list[ApplicationSchema]:
        """Получение списка всех сущностей Application."""
        return [_to_schema(application) for application in application_list_service()]

    def post(self, parsed_body: Body[ApplicationCreateSchema]) -> ApplicationSchema:
        """Создание новой сущности Application."""
        return _to_schema(
            application_create_service(
                payload=parsed_body,
            )
        )


@final
class ApplicationDetailController(Controller[MsgspecSerializer]):
    """Класс для взаиможействия с сущностью Application."""

    responses = (
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.NOT_FOUND,
        ),
    )

    def get(self, parsed_path: Path[ApplicationPathSchema]) -> ApplicationSchema:
        """Получение сущности Application по её ID."""
        return _to_schema(application_get_service(parsed_path.application_id))

    def put(
        self,
        parsed_path: Path[ApplicationPathSchema],
        parsed_body: Body[ApplicationSchema],
    ) -> ApplicationSchema:
        """Обновление существующей сущности Application по её ID."""
        return _to_schema(
            application_update_service(parsed_path.application_id, payload=parsed_body),
        )

    @modify(status_code=HTTPStatus.NO_CONTENT)
    def delete(self, parsed_path: Path[ApplicationPathSchema]) -> None:
        """Удаление сущности Application по её ID."""
        application_delete_service(parsed_path.application_id)

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, ApplicationNotFoundError):
            return self.to_error(
                self.format_error(
                    "Application not found",
                    error_type=ErrorType.value_error,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )
        return super().handle_error(endpoint, controller, exc)

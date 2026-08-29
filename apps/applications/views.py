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
    FormFieldSchema,
)
from .services import (
    CATEGORY_MAP,
    TECH_TASK_MAP,
    VISUAL_CONTENT_MAP,
    ApplicationNotFoundError,
    application_create_service,
    application_delete_service,
    application_get_service,
    application_list_service,
    application_update_service,
    get_form_structure_service,
    map_to_choice_items,
)


def _to_schema(application: Application) -> ApplicationSchema:
    return ApplicationSchema(
        id=application.id,
        full_name=application.full_name,
        group=application.group,
        birth_date=application.birth_date,
        telegram_url=application.telegram_url,
        vk_url=application.vk_url,
        github_url=application.github_url,
        portfolio_url=application.portfolio_url,
        categories=map_to_choice_items(application.categories or [], CATEGORY_MAP),
        tech_tasks=map_to_choice_items(application.tech_tasks or [], TECH_TASK_MAP),
        visual_content_types=map_to_choice_items(
            application.visual_content_types or [], VISUAL_CONTENT_MAP
        ),
    )


@final
class ApplicationFormSchemaController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с анкетой."""

    def get(self) -> list[FormFieldSchema]:
        """Получение структуры формы."""
        return get_form_structure_service()


@final
class ApplicationController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с коллекцией сущностей Application."""

    def get(self) -> list[ApplicationSchema]:
        """Получение списка всех сущностей Application."""
        return [_to_schema(application) for application in application_list_service()]

    def post(self, parsed_body: Body[ApplicationCreateSchema]) -> ApplicationSchema:
        """Создание новой сущности Application."""
        return _to_schema(application_create_service(payload=parsed_body))


@final
class ApplicationDetailController(Controller[MsgspecSerializer]):
    """Получение информации о сущности Application."""

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
        parsed_body: Body[ApplicationCreateSchema],
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

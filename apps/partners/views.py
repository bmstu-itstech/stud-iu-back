from http import HTTPStatus
from typing import final, override

from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from dmr import Body, Controller, Path, modify
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.metadata import ResponseSpec
from dmr.parsers import MultiPartParser
from dmr.plugins.msgspec import MsgspecJsonParser, MsgspecSerializer

from .serializers import PartnerCreateSchema, PartnerPathSchema, PartnerSchema
from .services import (
    PartnerNotFoundError,
    partner_create_service,
    partner_delete_service,
    partner_get_service,
    partner_list_service,
    partner_update_service,
)


def _to_schema(partner) -> PartnerSchema:
    return PartnerSchema(
        id=partner.pk,
        name=partner.name,
        url=partner.url,
        image=partner.image.url if partner.image else None,
    )


@final
class PartnerListController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с коллекцией сущностей Partner."""

    parsers = (
        MsgspecJsonParser(),
        MultiPartParser(),
    )

    def get(self) -> list[PartnerSchema]:
        """Получение списка всех сущностей Partner."""
        return [_to_schema(partner) for partner in partner_list_service()]

    def post(self, parsed_body: Body[PartnerCreateSchema]) -> PartnerSchema:
        """Создание новой сущности Partner."""
        image_file: UploadedFile | None = self.request.FILES.get("image")

        return _to_schema(
            partner_create_service(
                payload=parsed_body,
                image=image_file,
            )
        )


@final
class PartnerDetailController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с сущностью Partner."""

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

    def get(self, parsed_path: Path[PartnerPathSchema]) -> PartnerSchema:
        """Получение информации о сущности Partner по её ID."""
        return _to_schema(partner_get_service(parsed_path.partner_id))

    def put(
        self,
        parsed_path: Path[PartnerPathSchema],
        parsed_body: Body[PartnerCreateSchema],
    ) -> PartnerSchema:
        """Обновление информации о сущности Partner по её ID."""
        image_file: UploadedFile | None = self.request.FILES.get("logo")

        return _to_schema(
            partner_update_service(
                partner_id=parsed_path.partner_id,
                payload=parsed_body,
                image=image_file,
            )
        )

    @modify(status_code=HTTPStatus.NO_CONTENT)
    def delete(self, parsed_path: Path[PartnerPathSchema]) -> None:
        """Удаление сущности Partner по её ID."""
        partner_delete_service(parsed_path.partner_id)

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, PartnerNotFoundError):
            return self.to_error(
                self.format_error(
                    "Partner not found",
                    error_type=ErrorType.value_error,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )
        return super().handle_error(endpoint, controller, exc)

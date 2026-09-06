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

from .serializers import BoardMemberPathSchema, BoardMemberSchema
from .services import (
    BoardMemberNotFoundError,
    board_member_create_service,
    board_member_delete_service,
    board_member_get_service,
    board_member_list_service,
    board_member_update_service,
)


def _to_schema(board_member) -> BoardMemberSchema:
    return BoardMemberSchema(
        id=board_member.id,
        name=board_member.name,
        link=board_member.link,
        position=board_member.position,
        image=board_member.image.url if board_member.image else None,
    )


@final
class BoardMemberListController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с коллекцией сущностей BoardMember."""

    parsers = (
        MsgspecJsonParser(),
        MultiPartParser(),
    )

    def get(self) -> list[BoardMemberSchema]:
        """Получение списка всех сущностей BoardMember."""
        return [
            _to_schema(board_member) for board_member in board_member_list_service()
        ]

    def post(self, parsed_body: Body[BoardMemberSchema]) -> BoardMemberSchema:
        """Создание новой сущности BoardMember."""
        image_file: UploadedFile | None = self.request.FILES.get("image")

        return _to_schema(
            board_member_create_service(
                payload=parsed_body,
                image=image_file,
            )
        )


@final
class BoardMemberDetailController(Controller[MsgspecSerializer]):
    """Получение информации о сущности BoardMember."""

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

    def get(self, parsed_path: Path[BoardMemberPathSchema]) -> BoardMemberSchema:
        """Получение сущности BoardMember по её ID."""
        return _to_schema(board_member_get_service(parsed_path.board_member_id))

    def put(
        self,
        parsed_path: Path[BoardMemberPathSchema],
        parsed_body: Body[BoardMemberSchema],
    ) -> BoardMemberSchema:
        """Обновление существующей сущности BoardMember по её ID."""
        image_file: UploadedFile | None = self.request.FILES.get("image")

        return _to_schema(
            board_member_update_service(
                board_member_id=parsed_path.board_member_id,
                payload=parsed_body,
                image=image_file,
            ),
        )

    @modify(status_code=HTTPStatus.NO_CONTENT)
    def delete(self, parsed_path: Path[BoardMemberPathSchema]) -> None:
        """Удаление сущности BoardMember по её ID."""
        board_member_delete_service(parsed_path.board_member_id)

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, BoardMemberNotFoundError):
            return self.to_error(
                self.format_error(
                    "Board member not found",
                    error_type=ErrorType.value_error,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )
        return super().handle_error(endpoint, controller, exc)

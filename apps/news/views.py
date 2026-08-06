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

from .serializers import NewsCreateSchema, NewsPathSchema, NewsSchema
from .services import (
    NewsNotFoundError,
    news_create_service,
    news_delete_service,
    news_get_service,
    news_list_service,
    news_update_service,
)


def _to_schema(news) -> NewsSchema:
    return NewsSchema(
        id=news.pk,
        title=news.title,
        description=news.description,
        cover=news.cover.url if news.cover else None,
        created_at=news.created_at,
    )


@final
class NewsListController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с коллекцией сущностей News."""

    parsers = (
        MsgspecJsonParser(),
        MultiPartParser(),
    )

    def get(self) -> list[NewsSchema]:
        """Получение списка всех сущностей News."""
        return [_to_schema(news) for news in news_list_service()]

    def post(self, parsed_body: Body[NewsCreateSchema]) -> NewsSchema:
        """Создание новой сущности News."""
        cover_file: UploadedFile | None = self.request.FILES.get("cover")

        return _to_schema(
            news_create_service(
                payload=parsed_body,
                cover=cover_file,
            )
        )


@final
class NewsDetailController(Controller[MsgspecSerializer]):
    """Класс для взаимодействия с сущностью News."""

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

    def get(self, parsed_path: Path[NewsPathSchema]) -> NewsSchema:
        """Получение сущности News по её ID."""
        return _to_schema(news_get_service(parsed_path.news_id))

    def put(
        self,
        parsed_path: Path[NewsPathSchema],
        parsed_body: Body[NewsCreateSchema],
    ) -> NewsSchema:
        """Обновление существующей сущности News по её ID."""
        cover_file: UploadedFile | None = self.request.FILES.get("cover")

        return _to_schema(
            news_update_service(
                news_id=parsed_path.news_id,
                payload=parsed_body,
                cover=cover_file,
            ),
        )

    @modify(status_code=HTTPStatus.NO_CONTENT)
    def delete(self, parsed_path: Path[NewsPathSchema]) -> None:
        """Удаление сущности News по её ID."""
        news_delete_service(parsed_path.news_id)

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, NewsNotFoundError):
            return self.to_error(
                self.format_error(
                    "News not found",
                    error_type=ErrorType.value_error,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )
        return super().handle_error(endpoint, controller, exc)

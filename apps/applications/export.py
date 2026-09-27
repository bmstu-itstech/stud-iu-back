import csv
from http import HTTPStatus
from io import StringIO
from typing import final

from django.http import HttpResponse
from dmr import Controller, validate
from dmr.metadata import ResponseSpec
from dmr.plugins.msgspec import MsgspecSerializer

from apps.core.middleware import require_jwt_auth

from .jwt_service import EXPORT_SCOPE
from .models import Application
from .services import CATEGORY_MAP, TECH_TASK_MAP, VISUAL_CONTENT_MAP

CSV_HEADERS = (
    "ФИО",
    "Учебная группа",
    "Дата рождения",
    "Ссылка на Telegram",
    "Ссылка на VK",
    "GitHub",
    "Портфолио",
    "Виды деятельности",
    "Технические задачи",
    "Виды визуального контента",
)


def _labels(codes: list[str], mapping: dict[str, str]) -> str:
    """Коды выбранных опций → человекочитаемые подписи через «; »."""
    return "; ".join(mapping.get(code, code) for code in codes)


def _application_row(application: Application) -> list[str]:
    return [
        application.full_name,
        application.group,
        application.birth_date.isoformat(),
        application.telegram_url,
        application.vk_url,
        application.github_url or "",
        application.portfolio_url or "",
        _labels(application.categories or [], CATEGORY_MAP),
        _labels(application.tech_tasks or [], TECH_TASK_MAP),
        _labels(application.visual_content_types or [], VISUAL_CONTENT_MAP),
    ]


def _csv_response() -> HttpResponse:
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(CSV_HEADERS)
    for application in Application.objects.order_by("full_name", "group"):
        writer.writerow(_application_row(application))

    response = HttpResponse(
        buffer.getvalue().encode("utf-8-sig"),
        content_type="text/csv; charset=utf-8",
    )
    response["Content-Disposition"] = 'attachment; filename="applications.csv"'
    return response


@final
class FormsExportController(Controller[MsgspecSerializer]):

    @validate(
        ResponseSpec(
            bytes,
            status_code=HTTPStatus.OK,
            description="CSV-файл с анкетами активистов",
        ),
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.UNAUTHORIZED,
            description="Токен отсутствует или невалиден",
        ),
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.FORBIDDEN,
            description="Недостаточный scope токена",
        ),
        validate_responses=False,
    )
    @require_jwt_auth(scope=EXPORT_SCOPE)
    def get(self) -> HttpResponse:
        """GET /api/v0/application/forms/export/?token=<JWT> — выгрузка анкет в CSV."""
        return _csv_response()

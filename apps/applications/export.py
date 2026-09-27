import csv
from http import HTTPStatus
from io import StringIO

import jwt
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse

from .models import Application
from .services import CATEGORY_MAP, TECH_TASK_MAP, VISUAL_CONTENT_MAP

EXPORT_SCOPE = "forms_export"

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


def _error(detail: str, status: HTTPStatus) -> JsonResponse:
    return JsonResponse({"detail": detail}, status=status)


def forms_export_view(request: HttpRequest) -> HttpResponse:
    """GET /api/v0/forms/export/?token=<JWT> — выгрузка анкет в CSV.

    Токен подписывается HS256 секретом FORMS_EXPORT_JWT_SECRET и должен
    содержать claim scope = EXPORT_SCOPE.
    """
    token = request.GET.get("token")
    if not token:
        return _error("Token is missing", HTTPStatus.UNAUTHORIZED)

    try:
        payload = jwt.decode(
            token,
            settings.FORMS_EXPORT_JWT_SECRET,
            algorithms=["HS256"],
        )
    except jwt.InvalidTokenError:
        return _error("Invalid or expired token", HTTPStatus.UNAUTHORIZED)

    if payload.get("scope") != EXPORT_SCOPE:
        return _error("Token has insufficient scope", HTTPStatus.FORBIDDEN)

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(CSV_HEADERS)
    for application in Application.objects.order_by("full_name", "group"):
        writer.writerow(_application_row(application))

    # utf-8-sig: BOM в начале файла, чтобы Excel корректно открывал кириллицу
    response = HttpResponse(
        buffer.getvalue().encode("utf-8-sig"),
        content_type="text/csv; charset=utf-8",
    )
    response["Content-Disposition"] = 'attachment; filename="applications.csv"'
    return response

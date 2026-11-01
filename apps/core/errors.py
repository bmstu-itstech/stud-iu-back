from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from dmr import Controller
from dmr.errors import ErrorType


def validation_error_response(
    controller: Controller, exc: ValidationError
) -> HttpResponse:
    """Превращает ValidationError из Django в ответ 400 в формате dmr."""
    detail = [
        {"msg": messages[0], "loc": [field], "type": ErrorType.value_error}
        for field, messages in exc.message_dict.items()
    ]
    return controller.to_error(
        {"detail": detail},
        status_code=HTTPStatus.BAD_REQUEST,
    )

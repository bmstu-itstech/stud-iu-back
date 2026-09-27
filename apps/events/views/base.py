from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from dmr import Controller
from dmr.errors import ErrorType

from apps.events.serializers import EventImageSchema


def _images_to_schema(event) -> list[EventImageSchema]:
    return [
        EventImageSchema(id=img.pk, image=img.image.url if img.image else None)
        for img in event.images.all()
    ]


def _validation_error(controller: Controller, exc: ValidationError) -> HttpResponse:
    detail = [
        {"msg": messages[0], "loc": [field], "type": ErrorType.value_error}
        for field, messages in exc.message_dict.items()
    ]
    return controller.to_error({"detail": detail}, status_code=HTTPStatus.BAD_REQUEST)

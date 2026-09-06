from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet

from apps.core.serializers import DatabaseId

from .models import Partners
from .serializers import PartnerCreateSchema


class PartnerNotFoundError(Exception):
    """Возникает, когда сущность не найден в базе данных."""


def partner_list_service() -> QuerySet[Partners]:
    """Возвращает список всех сущностей Partner."""
    return Partners.objects.all()


def partner_get_service(partner_id: DatabaseId) -> Partners:
    """Возвращает сущность Partner по её ID.

    Если сущность не найдена, возникает ошибка PartnerNotFoundError.
    """
    try:
        return Partners.objects.get(pk=partner_id)
    except Partners.DoesNotExist:
        raise PartnerNotFoundError from None


def partner_create_service(
    payload: PartnerCreateSchema,
    image: UploadedFile | None = None,
) -> Partners:
    """Создаёт новую сущность Partner."""
    kwargs = {
        "name": payload.name,
        "url": payload.url,
    }

    if image is not None:
        kwargs["image"] = image

    return Partners.objects.create(**kwargs)


def partner_update_service(
    partner_id: DatabaseId,
    payload: PartnerCreateSchema,
    image: UploadedFile | None = None,
) -> Partners:
    """Обновляет существующую сущность Partner.

    Если сущность не найдена, возникает ошибка PartnerNotFoundError."""
    try:
        partner = Partners.objects.get(pk=partner_id)
    except Partners.DoesNotExist:
        raise PartnerNotFoundError from None

    partner.name = payload.name
    partner.url = payload.url

    if image is not None:
        partner.image = image

    partner.save()
    return partner


def partner_delete_service(partner_id: DatabaseId) -> None:
    """Удаляет существующую сущность Partner.

    Если сущность не найдена, возникает ошибка PartnerNotFoundError.
    """
    deleted, _ = Partners.objects.filter(pk=partner_id).delete()
    if not deleted:
        raise PartnerNotFoundError

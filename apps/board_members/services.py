from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet

from apps.core.serializers import DatabaseId

from .models import BoardMember
from .serializers import BoardMemberCreateSchema


class BoardMemberNotFoundError(Exception):
    """Возникает, когда сущность не найден в базе данных."""


def board_member_list_service() -> QuerySet[BoardMember]:
    """Возвращает список всех сущностей BoardMember."""
    return BoardMember.objects.all()


def board_member_get_service(board_member_id: DatabaseId) -> BoardMember:
    """Возвращает сущность BoardMember по её ID.

    Если сущность не найдена, возникает ошибка BoardMemberNotFoundError.
    """
    try:
        return BoardMember.objects.get(pk=board_member_id)
    except BoardMember.DoesNotExist:
        raise BoardMemberNotFoundError from None


def board_member_create_service(
    payload: BoardMemberCreateSchema,
    image: UploadedFile | None = None,
) -> BoardMember:
    """Создаёт новую сущность BoardMember."""
    kwargs = {
        "name": payload.name,
        "link": payload.link,
        "position": payload.position,
    }

    if image is not None:
        kwargs["image"] = image

    return BoardMember.objects.create(**kwargs)


def board_member_update_service(
    board_member_id: DatabaseId,
    payload: BoardMemberCreateSchema,
    image: UploadedFile | None = None,
) -> BoardMember:
    """Обновляет существующую сущность BoardMember."""
    board_member = board_member_get_service(board_member_id)

    board_member.name = payload.name
    board_member.link = payload.link
    board_member.position = payload.position

    if image is not None:
        board_member.image = image

    board_member.save()
    return board_member


def board_member_delete_service(board_member_id: DatabaseId) -> None:
    """Удаляет сущность BoardMember по её ID.

    Если сущность не найдена, возникает ошибка BoardMemberNotFoundError.
    """
    deleted, _ = BoardMember.objects.filter(pk=board_member_id).delete()
    if not deleted:
        raise BoardMemberNotFoundError

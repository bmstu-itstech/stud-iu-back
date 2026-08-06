import msgspec

from apps.core.serializers import DatabaseId


class BoardMemberPathSchema(msgspec.Struct):
    board_member_id: DatabaseId


class BoardMemberSchema(msgspec.Struct):
    """Схема для сущности BoardMember"""

    id: DatabaseId
    name: str
    link: str
    position: str
    image: str | None


class BoardMemberCreateSchema(msgspec.Struct):
    """Схема для создания сущности BoardMember"""

    name: str
    link: str
    position: str
    image: str | None = None

import msgspec

from apps.core.serializers import DatabaseId


class PartnerPathSchema(msgspec.Struct):
    partner_id: DatabaseId


class PartnerSchema(msgspec.Struct):
    """Схема для сущности Partner"""

    id: DatabaseId
    name: str
    url: str | None
    image: str | None


class PartnerCreateSchema(msgspec.Struct):
    """Схема для создания cущности Partner"""

    name: str
    url: str | None = None

import datetime as dt

import msgspec

from apps.core.serializers import DatabaseId


class ApplicationPathSchema(msgspec.Struct):
    application_id: DatabaseId


class ApplicationSchema(msgspec.Struct):
    """Схема для сущности Application"""

    id: DatabaseId
    full_name: str
    group: str
    birth_date: dt.date | None
    telegram_url: str | None
    vk_url: str | None
    github_url: str | None


class ApplicationCreateSchema(msgspec.Struct):
    """Схема для создания сущности Application"""

    full_name: str
    group: str
    birth_date: dt.date | None
    telegram_url: str | None
    vk_url: str | None
    github_url: str | None

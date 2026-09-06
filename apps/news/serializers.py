import datetime as dt

import msgspec

from apps.core.serializers import DatabaseId


class NewsPathSchema(msgspec.Struct):
    news_id: DatabaseId


class NewsSchema(msgspec.Struct):
    """Схема для сущности News"""

    id: DatabaseId
    title: str
    description: str
    cover: str | None
    created_at: dt.datetime


class NewsCreateSchema(msgspec.Struct):
    """Схема для создания cущности News"""

    title: str
    description: str = ""
    created_at: dt.datetime | None = None

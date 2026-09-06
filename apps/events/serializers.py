import msgspec

from apps.core.serializers import DatabaseId


class EventPathSchema(msgspec.Struct):
    event_id: DatabaseId


class EventImageSchema(msgspec.Struct):
    id: DatabaseId
    image: str | None


class EventSchema(msgspec.Struct):
    id: DatabaseId
    title: str
    description: str
    extended_description: str
    place: str
    precision: str
    start_datetime: str
    end_datetime: str | None
    date_range_display: str
    images: list[EventImageSchema]


class PastEventSchema(EventSchema):
    """Схема для сущности PastEvent"""

    album_link: str | None


class FutureEventSchema(EventSchema):
    """Схема для сущности FutureEvent"""

    registration_link: str | None


class EventCreateSchema(msgspec.Struct):
    title: str
    start_datetime: str
    description: str = ""
    extended_description: str = ""
    place: str = ""
    precision: str = "time"
    end_datetime: str | None = None


class PastEventCreateSchema(EventCreateSchema):
    """Схема для создания cущности PastEvent"""

    album_link: str | None = None


class FutureEventCreateSchema(EventCreateSchema):
    """Схема для создания cущности FutureEvent"""

    registration_link: str | None = None

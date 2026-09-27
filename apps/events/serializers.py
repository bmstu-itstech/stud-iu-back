from typing import Literal

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
    type: str
    start_datetime: str
    end_datetime: str | None
    date_range_display: str
    album_link: str | None
    registration_link: str | None
    images: list[EventImageSchema]


class EventCreateSchema(msgspec.Struct):
    title: str
    start_datetime: str
    type: Literal["past", "future"] = "future"
    description: str = ""
    extended_description: str = ""
    place: str = ""
    precision: str = "time"
    end_datetime: str | None = None
    album_link: str | None = None
    registration_link: str | None = None

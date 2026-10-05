import datetime as dt
from typing import Annotated

import msgspec

from apps.core.serializers import DatabaseId
from apps.events.enums import EventPeriod, EventSortField, SortOrder

EventDatetime = Annotated[
    str,
    msgspec.Meta(
        description=(
            "Дата в формате ISO 8601 или в обычном формате: "
            "14.03.2026 18:30, 14 марта 2026, 03.2026, 2026"
        ),
        examples=["2026-03-14T18:30:00+03:00", "14.03.2026 18:30", "март 2026"],
    ),
]

EventSlug = Annotated[
    str,
    msgspec.Meta(
        description="Читаемая ссылка на мероприятие",
        examples=["posvyat-v-studenty"],
    ),
]


class EventPathSchema(msgspec.Struct):
    event_ref: Annotated[
        str,
        msgspec.Meta(
            description="ID мероприятия или его читаемая ссылка",
            examples=["posvyat-v-studenty"],
        ),
    ]


class EventListQuerySchema(msgspec.Struct):
    period: EventPeriod | None = None
    sort: EventSortField = EventSortField.STARTED_AT
    order: SortOrder | None = None


class EventCreateSchema(msgspec.Struct, kw_only=True):
    """Схема для создания и обновления сущности Event"""

    title: str
    slug: EventSlug | None = None
    description: str = ""
    extended_description: str = ""
    place: str = ""
    precision: str
    start_datetime: EventDatetime
    end_datetime: EventDatetime | None = None
    album_link: str | None = None
    registration_link: str | None = None


class EventImageSchema(msgspec.Struct):
    id: DatabaseId
    image: str | None


class EventSchema(msgspec.Struct):
    """Схема для сущности Event"""

    id: DatabaseId
    slug: str
    title: str
    description: str
    extended_description: str
    place: str
    precision: str
    start_datetime: dt.datetime
    end_datetime: dt.datetime | None
    date_range_display: str
    images: list[EventImageSchema]
    album_link: str | None
    registration_link: str | None

from typing import Annotated

import msgspec

from apps.core.serializers import DatabaseId
from apps.events.enums import EventPeriod, EventSortField, SortOrder

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
    start_datetime: str
    end_datetime: str | None = None
    album_link: str | None = None
    registration_link: str | None = None


class EventImageSchema(msgspec.Struct):
    id: DatabaseId
    image: str | None


class EventSchema(msgspec.Struct):
    """Схема для сущности Event"""

    id: DatabaseId
    slug: str | None
    title: str
    description: str
    extended_description: str
    place: str
    precision: str
    start_datetime: Annotated[
        str,
        msgspec.Meta(
            description="Дата начала в том же формате, что и при создании",
            examples=["14.03.2027 18:00"],
        ),
    ]
    end_datetime: str | None
    date_range: Annotated[
        str,
        msgspec.Meta(
            description="Даты проведения для отображения на сайте",
            examples=["14 марта 2027 18:00-21:30"],
        ),
    ]
    images: list[EventImageSchema]
    album_link: str | None
    registration_link: str | None

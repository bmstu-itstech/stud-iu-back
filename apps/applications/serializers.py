import datetime as dt
from enum import StrEnum

import msgspec

from apps.core.serializers import DatabaseId


class ApplicationPathSchema(msgspec.Struct):
    application_id: DatabaseId


class FieldType(StrEnum):
    TEXT = "text"
    DATE = "date"
    URL = "url"
    MULTIPLE_CHOICE = "multiple_choice"


class OptionSchema(msgspec.Struct):
    value: str
    label: str


class DependencySchema(msgspec.Struct):
    field: str
    contains: str


class FormFieldSchema(msgspec.Struct):
    """Описание одного поля анкеты"""

    key: str
    label: str
    type: FieldType
    required: bool = False
    placeholder: str | None = None
    pattern: str | None = None
    options: list[OptionSchema] | None = None
    depends_on: DependencySchema | None = None


class ChoiceItemSchema(msgspec.Struct):
    value: str
    label: str


class ApplicationSchema(msgspec.Struct):
    """Схема для сущности Application"""

    id: DatabaseId
    full_name: str
    group: str
    birth_date: dt.date
    telegram_url: str
    vk_url: str
    github_url: str | None
    portfolio_url: str | None

    categories: list[ChoiceItemSchema]
    tech_tasks: list[ChoiceItemSchema]
    visual_content_types: list[ChoiceItemSchema]


class ApplicationCreateSchema(msgspec.Struct):
    """Схема для создания сущности Application"""

    full_name: str
    group: str
    birth_date: dt.date
    telegram_url: str
    vk_url: str
    github_url: str | None = None
    portfolio_url: str | None = None

    categories: list[str] = msgspec.field(default_factory=list)
    tech_tasks: list[str] = msgspec.field(default_factory=list)
    visual_content_types: list[str] = msgspec.field(default_factory=list)

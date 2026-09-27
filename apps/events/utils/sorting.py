from collections.abc import Iterable
from datetime import datetime

from dateutil.parser import parse

from apps.events.enums import EventSortField, SortOrder
from apps.events.models import Events

_DEFAULT_DATE = datetime(2000, 1, 1)


def parse_event_date(date_str: str | None) -> datetime | None:
    if not date_str:
        return None

    try:
        return parse(date_str, dayfirst=True, fuzzy=True, default=_DEFAULT_DATE)
    except ValueError, OverflowError:
        return None


def _sort_key(
    event: Events, sort: EventSortField, order: SortOrder
) -> tuple[bool, float]:
    date = None
    if sort == EventSortField.ENDED_AT:
        date = parse_event_date(event.end_datetime)
    date = date or parse_event_date(event.start_datetime)

    if date is None:
        return True, 0

    timestamp = date.timestamp()
    return False, -timestamp if order == SortOrder.DESC else timestamp


def sort_events(
    events: Iterable[Events], sort: EventSortField, order: SortOrder
) -> list[Events]:
    return sorted(events, key=lambda event: _sort_key(event, sort, order))

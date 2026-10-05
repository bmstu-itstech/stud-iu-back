import uuid
from datetime import datetime

from dateutil.parser import ParserError, parse
from django.db import migrations

from apps.events.utils import parse_date, period_end, to_local, truncate_date

_FALLBACK_START = datetime(2000, 1, 1)


def copy_events(apps, schema_editor):
    FutureEvents = apps.get_model("events", "FutureEvents")
    PastEvents = apps.get_model("events", "PastEvents")
    Events = apps.get_model("events", "Events")
    EventImages = apps.get_model("events", "EventImages")

    unparsed = []
    used_ids = set()

    for Model, image_field, link_field in (
        (FutureEvents, "future_event", "registration_link"),
        (PastEvents, "past_event", "album_link"),
    ):
        for old in Model.objects.all():
            start = _parse_old_date(old.start_datetime)
            end = _parse_old_date(old.end_datetime)
            if start is None:
                start = to_local(_FALLBACK_START)
                unparsed.append(f"\"{old.title}\": {old.start_datetime!r}")
            start = truncate_date(start, old.precision)
            end = truncate_date(end, old.precision)

            new_id = old.pk if old.pk not in used_ids else uuid.uuid4()
            used_ids.add(new_id)

            Events.objects.create(
                id=new_id,
                title=old.title,
                description=old.description,
                extended_description=old.extended_description,
                place=old.place,
                precision=old.precision,
                start_datetime=start,
                end_datetime=end,
                finished_at=period_end(end or start, old.precision),
                **{link_field: getattr(old, link_field)},
            )
            EventImages.objects.filter(**{image_field: old.pk}).update(event_id=new_id)

    if unparsed:
        print("Требует исправления:\n", "\n".join(unparsed))


def _parse_old_date(value):
    try:
        return parse_date(value)
    except ValueError:
        pass

    try:
        return to_local(parse(value, dayfirst=True, fuzzy=True))
    except (ParserError, ValueError, OverflowError):
        return None


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_events_unified"),
    ]

    operations = [
        migrations.RunPython(copy_events, migrations.RunPython.noop),
    ]

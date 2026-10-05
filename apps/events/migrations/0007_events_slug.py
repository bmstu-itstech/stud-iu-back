from django.db import migrations, models

from apps.events.utils import SLUG_MAX_LENGTH, make_slug


def fill_slugs(apps, schema_editor):
    Events = apps.get_model("events", "Events")
    used = set()
    for event in Events.objects.order_by("start_datetime", "pk"):
        base = make_slug(event.title) or "event"
        slug, number = base, 1
        while slug in used:
            number += 1
            slug = f"{base[: SLUG_MAX_LENGTH - 4]}-{number}"
        used.add(slug)
        event.slug = slug
        event.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_remove_old_events"),
    ]

    operations = [
        migrations.AddField(
            model_name="events",
            name="slug",
            field=models.SlugField(blank=True, db_index=False, default="", max_length=SLUG_MAX_LENGTH, verbose_name="Короткая ссылка"),
            preserve_default=False,
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="events",
            name="slug",
            field=models.SlugField(blank=True, error_messages={"unique": "Мероприятие с такой ссылкой уже существует"}, max_length=SLUG_MAX_LENGTH, unique=True, verbose_name="Короткая ссылка"),
        ),
    ]

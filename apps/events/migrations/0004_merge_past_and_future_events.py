import uuid

import django.db.models.deletion
from django.db import migrations, models


def copy_events_to_unified(apps, schema_editor):
    future_events = apps.get_model("events", "FutureEvents")
    past_events = apps.get_model("events", "PastEvents")
    events = apps.get_model("events", "Events")

    for old in future_events.objects.all():
        events.objects.create(
            id=old.id,
            title=old.title,
            description=old.description,
            extended_description=old.extended_description,
            place=old.place,
            precision=old.precision,
            type="future",
            start_datetime=old.start_datetime,
            start_date=old.start_date,
            end_datetime=old.end_datetime,
            registration_link=old.registration_link,
        )
    for old in past_events.objects.all():
        events.objects.create(
            id=old.id,
            title=old.title,
            description=old.description,
            extended_description=old.extended_description,
            place=old.place,
            precision=old.precision,
            type="past",
            start_datetime=old.start_datetime,
            start_date=old.start_date,
            end_datetime=old.end_datetime,
            album_link=old.album_link,
        )


def copy_event_images(apps, schema_editor):
    event_images = apps.get_model("events", "EventImages")
    for image in event_images.objects.all():
        event_id = image.past_event_id or image.future_event_id
        if event_id:
            event_images.objects.filter(pk=image.pk).update(event_id=event_id)


def revert_noop(apps, schema_editor):
  pass

class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_futureevents_start_date_pastevents_start_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Events",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=256, verbose_name="Название")),
                ("description", models.CharField(blank=True, max_length=256, verbose_name="Описание")),
                ("extended_description", models.TextField(blank=True, help_text="Развёрнутое описание для подраздела             «О мероприятии» на странице мероприятия", verbose_name="Развёрнутое описание")),
                ("place", models.CharField(blank=True, max_length=256, verbose_name="Место проведения")),
                ("precision", models.CharField(choices=[("year", "Год"), ("month", "Месяц"), ("day", "День"), ("time", "Время")], default="time", max_length=10, verbose_name="Точность")),
                ("type", models.CharField(choices=[("past", "Прошедшее"), ("future", "Запланированное")], default="future", help_text="Прошедшее или запланированное мероприятие", max_length=10, verbose_name="Тип мероприятия")),
                ("start_datetime", models.CharField(help_text="Дата начала мероприятия, например, 11.05.2006", max_length=40, verbose_name="Дата начала")),
                ("start_date", models.DateTimeField(blank=True, editable=False, help_text="Заполняется автоматически из «Дата начала» при сохранении, используется для сортировки на уровне БД", null=True, verbose_name="Дата начала (нормализованная)")),
                ("end_datetime", models.CharField(blank=True, help_text="Дата конца мероприятия, например, 11.05.2006", max_length=40, null=True, verbose_name="Дата конца")),
                ("album_link", models.URLField(blank=True, null=True, verbose_name="Ссылка на альбом")),
                ("registration_link", models.URLField(blank=True, null=True, verbose_name="Ссылка на регистрацию")),
            ],
        ),
        migrations.RunPython(copy_events_to_unified, revert_noop),
        migrations.RemoveConstraint(
            model_name="eventimages",
            name="only_one_event_link",
        ),
        migrations.AddField(
            model_name="eventimages",
            name="event",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="images", to="events.events"),
        ),
        migrations.RunPython(copy_event_images, revert_noop),
        migrations.AlterField(
            model_name="eventimages",
            name="event",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="events.events"),
        ),
        migrations.RemoveField(
            model_name="eventimages",
            name="past_event",
        ),
        migrations.RemoveField(
            model_name="eventimages",
            name="future_event",
        ),
        migrations.DeleteModel(
            name="FutureEvents",
        ),
        migrations.DeleteModel(
            name="PastEvents",
        ),
    ]

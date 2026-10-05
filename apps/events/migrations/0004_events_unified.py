import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_alter_futureevents_extended_description_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Events",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=256, verbose_name="Название")),
                ("description", models.CharField(blank=True, max_length=256, verbose_name="Описание")),
                ("extended_description", models.TextField(blank=True, help_text="Развёрнутое описание для подраздела «О мероприятии» на странице мероприятия", verbose_name="Развёрнутое описание")),
                ("place", models.CharField(blank=True, max_length=256, verbose_name="Место проведения")),
                ("precision", models.CharField(choices=[("year", "Год"), ("month", "Месяц"), ("day", "День"), ("time", "Время")], default="time", max_length=10, verbose_name="Точность")),
                ("start_datetime", models.DateTimeField(help_text="Дата и время начала мероприятия", verbose_name="Дата начала")),
                ("end_datetime", models.DateTimeField(blank=True, help_text="Дата и время конца мероприятия", null=True, verbose_name="Дата конца")),
                ("finished_at", models.DateTimeField(db_index=True, editable=False, verbose_name="Конец периода с учётом точности")),
                ("registration_link", models.URLField(blank=True, null=True, verbose_name="Ссылка на регистрацию")),
                ("album_link", models.URLField(blank=True, null=True, verbose_name="Ссылка на альбом")),
            ],
            options={
                "verbose_name": "Мероприятие",
                "verbose_name_plural": "Мероприятия",
            },
        ),
        migrations.AddField(
            model_name="eventimages",
            name="event",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name="images", to="events.events", verbose_name="Мероприятие"),
        ),
    ]

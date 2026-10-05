import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_copy_events_data"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="eventimages",
            name="only_one_event_link",
        ),
        migrations.RemoveField(
            model_name="eventimages",
            name="future_event",
        ),
        migrations.RemoveField(
            model_name="eventimages",
            name="past_event",
        ),
        migrations.AlterField(
            model_name="eventimages",
            name="event",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="events.events", verbose_name="Мероприятие"),
        ),
        migrations.AlterModelOptions(
            name="eventimages",
            options={"verbose_name": "Изображение мероприятия", "verbose_name_plural": "Изображения мероприятий"},
        ),
        migrations.DeleteModel(
            name="FutureEvents",
        ),
        migrations.DeleteModel(
            name="PastEvents",
        ),
    ]

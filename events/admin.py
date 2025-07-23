from django.contrib import admin
from events.models import PastEvents, FutureEvents


@admin.register(PastEvents)
class PastEventsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'precision',
        'start_datetime',
        'end_datetime',
        'album_link',
    )


@admin.register(FutureEvents)
class FutureEventsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'precision',
        'start_datetime',
        'end_datetime',
        'registration_link',
    )

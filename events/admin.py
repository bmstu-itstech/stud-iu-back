from django.contrib import admin
from events.models import PastEvents, FutureEvents, EventImages


class PastEventImagesInline(admin.TabularInline):
    model = EventImages
    fk_name = 'past_event'
    extra = 1
    exclude = ('future_event',)


class FutureEventImagesInline(admin.TabularInline):
    model = EventImages
    fk_name = 'future_event'
    extra = 1
    exclude = ('past_event',)


@admin.register(PastEvents)
class PastEventsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'place',
        'color',
        'precision',
        'start_datetime',
        'end_datetime',
        'album_link',
    )

    inlines = [PastEventImagesInline,]


@admin.register(FutureEvents)
class FutureEventsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'place',
        'color',
        'precision',
        'start_datetime',
        'end_datetime',
        'registration_link',
    )

    inlines = [FutureEventImagesInline,]

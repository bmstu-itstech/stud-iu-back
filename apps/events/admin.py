from django.contrib import admin

from .models import EventImages, FutureEvents, PastEvents


class PastEventImagesInline(admin.TabularInline):
    model = EventImages
    fk_name = "past_event"
    extra = 1
    fields = ("image",)


class FutureEventImagesInline(admin.TabularInline):
    model = EventImages
    fk_name = "future_event"
    extra = 1
    fields = ("image",)


@admin.register(PastEvents)
class PastEventsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "place",
        "get_date_range",
        "precision",
        "has_album",
        "images_count",
    )
    search_fields = ("title", "description", "place")
    inlines = [PastEventImagesInline]

    @admin.display(description="Даты проведения")
    def get_date_range(self, obj):
        return obj.date_range_display

    @admin.display(description="Альбом", boolean=True)
    def has_album(self, obj):
        return bool(obj.album_link)

    @admin.display(description="Фото")
    def images_count(self, obj):
        return obj.images.count()


@admin.register(FutureEvents)
class FutureEventsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "place",
        "get_date_range",
        "precision",
        "has_registration",
        "images_count",
    )
    search_fields = ("title", "description", "place")
    inlines = [FutureEventImagesInline]

    @admin.display(description="Даты проведения")
    def get_date_range(self, obj):
        return obj.date_range_display

    @admin.display(description="Регистрация", boolean=True)
    def has_registration(self, obj):
        return bool(obj.registration_link)

    @admin.display(description="Фото")
    def images_count(self, obj):
        return obj.images.count()

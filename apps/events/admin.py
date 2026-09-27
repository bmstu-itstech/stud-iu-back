from django.contrib import admin

from .models import EventImages, Events


class EventImagesInline(admin.TabularInline):
    model = EventImages
    fk_name = "event"
    extra = 1
    fields = ("image",)


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "place",
        "get_date_range",
        "precision",
        "has_album",
        "has_registration",
        "images_count",
    )
    list_filter = ("type",)
    search_fields = ("title", "description", "place")
    inlines = [EventImagesInline]

    @admin.display(description="Даты проведения")
    def get_date_range(self, obj):
        return obj.date_range_display

    @admin.display(description="Альбом", boolean=True)
    def has_album(self, obj):
        return bool(obj.album_link)

    @admin.display(description="Регистрация", boolean=True)
    def has_registration(self, obj):
        return bool(obj.registration_link)

    @admin.display(description="Фото")
    def images_count(self, obj):
        return obj.images.count()

from django.contrib import admin

from .models import EventImages, Events


class EventImagesInline(admin.TabularInline):
    model = EventImages
    extra = 1
    fields = ("image",)


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "place",
        "get_date_range",
        "precision",
        "has_registration",
        "has_album",
        "images_count",
    )
    search_fields = ("title", "slug", "description", "place")
    ordering = ("-start_datetime",)
    inlines = [EventImagesInline]

    @admin.display(description="Даты проведения", ordering="start_datetime")
    def get_date_range(self, obj: Events) -> str:
        return obj.date_range_display

    @admin.display(description="Регистрация", boolean=True)
    def has_registration(self, obj: Events) -> bool:
        return bool(obj.registration_link)

    @admin.display(description="Альбом", boolean=True)
    def has_album(self, obj: Events) -> bool:
        return bool(obj.album_link)

    @admin.display(description="Фото")
    def images_count(self, obj: Events) -> int:
        return obj.images.count()

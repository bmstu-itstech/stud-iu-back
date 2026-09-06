from django.contrib import admin

from .models import Partners


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url", "image_url")
    search_fields = ("id", "name", "url")

    @admin.display(description="Изображение")
    def image_url(self, obj: Partners) -> str | None:
        return obj.image.name if obj.image else None

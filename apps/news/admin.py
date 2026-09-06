from django.contrib import admin

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "cover_url", "created_at")
    search_fields = ("id", "title", "description")
    ordering = ("-created_at",)

    @admin.display(description="Обложка")
    def cover_url(self, obj: News) -> str | None:
        return obj.cover.name if obj.cover else None

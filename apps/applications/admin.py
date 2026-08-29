from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "group",
        "display_categories",
        "birth_date",
        "telegram_url",
    )
    search_fields = ("full_name", "group", "telegram_url")
    ordering = ("full_name",)

    @admin.display(description="Направления")
    def display_categories(self, obj: Application) -> str:
        return ", ".join(obj.categories) if obj.categories else "-"

from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "full_name",
        "group",
        "telegram",
        "phone",
        "display_categories",
        "birth_date",
    )
    search_fields = ("full_name", "group", "telegram")
    ordering = ("-created_at",)

    @admin.display(description="Направления")
    def display_categories(self, obj: Application) -> str:
        return ", ".join(obj.categories) if obj.categories else "-"

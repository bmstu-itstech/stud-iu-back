from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "group",
        "birth_date",
        "telegram_url",
        "vk_url",
        "github_url",
    )
    search_fields = (
        "id",
        "full_name",
        "group",
        "birth_date",
        "telegram_url",
        "vk_url",
        "github_url",
    )
    ordering = ("full_name",)

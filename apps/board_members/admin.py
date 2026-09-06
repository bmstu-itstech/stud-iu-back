from django.contrib import admin

from .models import BoardMember


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "link", "position", "image_url")
    search_fields = ("id", "name", "link", "position")

    @admin.display(description="Изображение")
    def image_url(self, obj: BoardMember) -> str | None:
        return obj.image.name if obj.image else None

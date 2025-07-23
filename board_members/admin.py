from django.contrib import admin
from board_members.models import BoardMember


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'telegram_link',
        'position',
        'start_date',
        'description',
        'image',
    )

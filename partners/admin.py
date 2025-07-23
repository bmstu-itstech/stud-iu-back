from django.contrib import admin

from partners.models import Partners


@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'url',
        'image',
    )

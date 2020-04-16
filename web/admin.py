from django.contrib import admin
from .models import Color

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'hex_code',
    )

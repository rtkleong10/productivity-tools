from django.contrib import admin
from .models import Activity, ActivityEvent

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'frequency',
        'user',
        'days_since',
    )

    def is_frequency_exceeded(self, instance):
        return instance.is_frequency_exceeded

    is_frequency_exceeded.boolean = True

@admin.register(ActivityEvent)
class ActivityEventAdmin(admin.ModelAdmin):
    list_display = (
        'activity',
        'event_type',
        'date',
    )
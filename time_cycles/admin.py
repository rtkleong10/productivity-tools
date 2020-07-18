from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from .models import Cycle, Timer

@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
	list_display = (
		'title',
		'user',
	)

@admin.register(Timer)
class TimerAdmin(OrderedModelAdmin):
	list_display = (
		'title',
		'duration',
		'cycle',
		'order',
		'move_up_down_links',
	)

	ordering = (
		'cycle',
		'order',
	)

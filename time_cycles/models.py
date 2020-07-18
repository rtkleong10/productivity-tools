import uuid
from datetime import timedelta
from django.conf import settings
from django.db import models
from common.models import Color
from ordered_model.models import OrderedModel

class Cycle(models.Model):
	id = models.UUIDField(
		help_text='Unique identifier',
		primary_key=True,
		default=uuid.uuid4,
		editable=False,
	)

	title = models.CharField(
		help_text='Identifies the cycle.',
		max_length=200,
	)

	user = models.ForeignKey(
		help_text='The user this cycle belongs to.',
		to=settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)

	created_at = models.DateTimeField(
		help_text='When the cycle is created.',
		auto_now_add=True,
	)

	@property
	def total_duration(self):
		total_duration = timedelta()

		for timer in self.timers.all():
			total_duration += timer.duration

		return total_duration

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('created_at',)

class Timer(OrderedModel):
	id = models.UUIDField(
		help_text='Unique identifier',
		primary_key=True,
		default=uuid.uuid4,
		editable=False,
	)

	cycle = models.ForeignKey(
		help_text='The cycle the timer is for.',
		to=Cycle,
		related_name='timers',
		on_delete=models.CASCADE,
	)

	title = models.CharField(
		help_text='Identifies the timer.',
		max_length=200,
	)

	duration = models.DurationField(
		help_text='The duration of the timer.'
	)

	color = models.ForeignKey(
		help_text='Colour attached to the timer.',
		to=Color,
		on_delete=models.PROTECT,
	)

	order_with_respect_to = 'cycle'

	def __str__(self):
		return "{} - {}".format(self.cycle, self.title)

	class Meta:
		ordering = ('order',)
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from common.models import Color
from django.core.validators import MinValueValidator
import datetime

class Activity(models.Model):
	id = models.UUIDField(
		help_text='Unique identifier',
		primary_key=True,
		default=uuid.uuid4,
		editable=False,
	)

	title = models.CharField(
		help_text='Identifies the activity.',
		max_length=200,
	)

	description = models.TextField(
		help_text='Describes the activity.',
		blank=True,
	)

	frequency = models.PositiveIntegerField(
		help_text='Ideal maximum frequency of the activity in days. If the days since the activity is last performed exceeds the frequency, an alert may be provided.',
		validators=(MinValueValidator(1),),
		verbose_name='frequency (in days)',
		null=True,
	)

	user = models.ForeignKey(
		help_text='The user this activity belongs to.',
		to=settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)

	created_at = models.DateTimeField(
		help_text='When the activity is created.',
		auto_now_add=True,
	)

	color = models.ForeignKey(
		help_text='Colour attached to the activity',
		to=Color,
		on_delete=models.PROTECT,
	)

	@property
	def todays_event(self):
		tzinfo = self.user.profile.timezone if self.user.profile else settings.TIME_ZONE
		today = timezone.localdate(timezone=tzinfo)
		todays_event = self.events.filter(date=today).first()
		return todays_event.event_type if todays_event else None

	@property
	def last_event(self):
		last_event = self.events.order_by('date').last()
		return last_event

	@property
	def last_event_type(self):
		last_event = self.last_event
		return last_event.event_type if last_event else None

	@property
	def days_since(self):
		tzinfo = self.user.profile.timezone if self.user.profile else settings.TIME_ZONE
		last_event = self.last_event

		if last_event:
			last_event_date = last_event.date
		else:
			last_event_date = timezone.localdate(value=self.created_at, timezone=tzinfo)

		today = timezone.localdate(timezone=tzinfo)
		days_since = (today - last_event_date).days
		return days_since

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'activities'
		ordering = ('created_at',)

class ActivityEvent(models.Model):
	COMPLETED = 1
	SKIPPED = 2
	EVENT_TYPES = [
		(COMPLETED, 'Completed'),
		(SKIPPED, 'Skipped'),
	]

	id = models.UUIDField(
		help_text='Unique identifier',
		primary_key=True,
		default=uuid.uuid4,
		editable=False,
	)

	activity = models.ForeignKey(
		help_text='The activity the event is for.',
		to=Activity,
		related_name='events',
		on_delete=models.CASCADE,
	)

	date = models.DateField(
		help_text='The date of the event.',
		default=datetime.date.today,
	)

	event_type = models.PositiveSmallIntegerField(
		help_text='The type of event.',
		choices=EVENT_TYPES,
		default=COMPLETED,
	)

	description = models.TextField(
		help_text='Describes the event.',
		blank=True,
	)

	def __str__(self):
		return '{}  {}'.format(self.get_event_type_display(), self.activity.title)

	class Meta:
		ordering = ('-date',)
		unique_together = ('activity', 'date')
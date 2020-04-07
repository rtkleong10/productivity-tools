from django.conf import settings
from django.db import models
from django.utils import timezone

class Activity(models.Model):
	title = models.CharField(
		help_text='Identifies the activity.',
		max_length=200,
	)

	description = models.TextField(
		help_text='Describes the activity.',
		blank=True,
	)

	frequency = models.PositiveIntegerField(
		help_text='Ideal maximum frequency of the activity in days. If the days since the activity is last performed exceeds the frequency, an alert may be provided.'
	)

	user = models.ForeignKey(
		help_text='The user this activity belongs to.',
		to=settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)

	@property
	def last_event_date_time(self):
		last_event = self.events.order_by('date_time').last()
		return last_event.date_time if last_event else None

	@property
	def days_since(self):
		last_event_date_time = self.last_event_date_time

		if not last_event_date_time:
			return 0

		last_event_date = last_event_date_time.date()
		today = timezone.now().date()
		days_since = (today - last_event_date).days
		return days_since

	@property
	def is_frequency_exceeded(self):
		return self.days_since > self.frequency

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'activities'

class ActivityEvent(models.Model):
	COMPLETED = 1
	SKIPPED = 2
	CREATED = 3
	EVENT_TYPES = [
		(COMPLETED, 'Completed'),
		(SKIPPED, 'Skipped'),
		(CREATED, 'Created'),
	]

	activity = models.ForeignKey(
		help_text='The activity the event is for.',
		to=Activity,
		related_name='events',
		on_delete=models.CASCADE,
	)

	date_time = models.DateTimeField(
		help_text='The date and time of the event.',
	)

	event_type = models.PositiveSmallIntegerField(
		help_text='The type of event.',
		choices=EVENT_TYPES,
		default=COMPLETED,
	)

	def __str__(self):
		return '{}  {}'.format(self.get_event_type_display(), self.activity.title)
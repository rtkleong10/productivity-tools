from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from api.models import Activity, ActivityEvent
from django.views.generic.edit import CreateView, UpdateView, DeleteView

__all__ = [
	'home_view',
	'activity_detail',
	'complete_activity',
	'skip_activity',
	'CreateActivity',
	'UpdateActivity',
	'DeleteActivity',
	'CreateEvent',
	'UpdateEvent',
	'DeleteEvent',
]

class Mixin():
	def get_context_data(self, **kwargs):
		"""Add the models verbose name to the context dictionary."""
		kwargs.update({
			"verbose_name": self.form_class._meta.model._meta.verbose_name,})
		return super().get_context_data(**kwargs)

@login_required
@require_http_methods(["GET"])
def home_view(request):
	user = request.user
	activities = Activity.objects.filter(user=user)
	tzinfo = user.profile.timezone if user.profile else settings.TIME_ZONE
	today = timezone.localdate(timezone=tzinfo)

	context = {
		'today': today,
		'activities': activities,
	}
	return render(request, 'web/home.html', context)

class CreateActivity(LoginRequiredMixin, CreateView):
	model = Activity
	fields = (
		'title',
		'description',
		'frequency',
	)
	template_name = 'web/model_form.html'
	success_url = reverse_lazy('web:home')
	extra_context = {
		'model_name': 'Activity'
	}

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class UpdateActivity(LoginRequiredMixin, UpdateView):
	model = Activity
	fields = (
		'title',
		'description',
		'frequency',
	)
	template_name = 'web/model_form.html'
	extra_context = {
		'model_name': 'Activity'
	}

	def get_success_url(self):
		return reverse('web:activity-detail', kwargs={'pk': self.object.pk})

class DeleteActivity(LoginRequiredMixin, DeleteView):
	model = Activity
	template_name = 'web/delete_form.html'
	success_url = reverse_lazy('web:home')

@login_required
@require_http_methods(["GET"])
def activity_detail(request, pk):
	user = request.user
	activity = get_object_or_404(Activity, user=user, pk=pk)

	context = {
		'activity': activity,
	}
	return render(request, 'web/activity_detail.html', context)

@login_required
@require_http_methods(["POST"])
def complete_activity(request, pk):
	user = request.user
	tzinfo = user.profile.timezone if user.profile else settings.TIME_ZONE
	activity = get_object_or_404(Activity, user=user, pk=pk)

	activity.events.create(
		date=timezone.localdate(timezone=tzinfo),
		event_type=ActivityEvent.COMPLETED,
	)

	return redirect('web:home')

@login_required
@require_http_methods(["POST"])
def skip_activity(request, pk):
	user = request.user
	tzinfo = user.profile.timezone if user.profile else settings.TIME_ZONE
	activity = get_object_or_404(Activity, user=user, pk=pk)

	activity.events.create(
		date=timezone.localdate(timezone=tzinfo),
		event_type=ActivityEvent.SKIPPED,
	)

	return redirect('web:home')

class CreateEvent(LoginRequiredMixin, CreateView):
	model = ActivityEvent
	fields = (
		'date',
		'event_type',
	)
	template_name = 'web/model_form.html'
	extra_context = {
		'model_name': 'Event'
	}

	def dispatch(self, request, *args, **kwargs):
		self.activity = get_object_or_404(Activity, pk=kwargs['activity'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.instance.activity = self.activity
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('web:activity-detail', kwargs={'pk': self.object.activity.pk})

class UpdateEvent(LoginRequiredMixin, UpdateView):
	model = ActivityEvent
	fields = (
		'date',
		'event_type',
	)
	template_name = 'web/model_form.html'
	extra_context = {
		'model_name': 'Event'
	}

	def get_success_url(self):
		return reverse('web:activity-detail', kwargs={'pk': self.object.activity.pk})

class DeleteEvent(LoginRequiredMixin, DeleteView):
	model = ActivityEvent
	template_name = 'web/delete_form.html'
	extra_context = {
		'model_name': 'Event'
	}

	def get_success_url(self):
		return reverse('web:activity-detail', kwargs={'pk': self.object.activity.pk})
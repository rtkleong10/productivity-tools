from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Cycle, Timer
from rest_framework import serializers
from .serializers import CycleListSerializer, CycleDetailSerializer, TimerListSerializer, TimerDetailSerializer, TimerMoveSerializer

class CycleViewSet(viewsets.ModelViewSet):
	"""
	A cycle is a sequence of timers.

	# Fields
	- Title
	"""
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		return Cycle.objects.filter(user=user).order_by('created_at')

	def get_serializer_class(self):
		if self.action == 'list':
			return CycleListSerializer
		else:
			return CycleDetailSerializer

	def perform_create(self, serializer):
		user = self.request.user
		serializer.save(user=user)

class TimerViewSet(viewsets.ModelViewSet):
	"""
	Timers are used to represent timed tasks within a cycle. To reorder the timers,

	# Fields
	- Title
	- Duration (format: `[DD] [[HH:]MM:]ss[.uuuuuu]`)
	- Color (color refers to the id of the color in the colors list)

	# Reordering Timers
	- Use the extra actions (move down & move up) in the detail page
	- Need to do a POST request (can leave the body empty)
	"""
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		cycle = get_object_or_404(Cycle, pk=self.kwargs['cycle'], user=user)
		return Timer.objects.filter(cycle=cycle).order_by('order')

	def get_serializer_class(self):
		if self.action == 'list':
			return TimerListSerializer
		elif self.action in ['move_up', 'move_down']:
			return TimerMoveSerializer
		else:
			return TimerDetailSerializer

	def perform_create(self, serializer):
		user = self.request.user
		cycle = get_object_or_404(Cycle, pk=self.kwargs['cycle'], user=user)

		serializer.save(cycle=cycle)

	@action(detail=True, methods=["POST"], url_path="move-up", url_name="moveup")
	def move_up(self, request, *args, **kwargs):
		user = request.user
		timer = get_object_or_404(Timer, pk=kwargs['pk'], cycle=kwargs['cycle'], cycle__user=user)
		timer.up()

		return self.list(self, request, *args, **kwargs)

	@action(detail=True, methods=["POST"], url_path="move-down", url_name="movedown")
	def move_down(self, request, *args, **kwargs):
		user = request.user
		timer = get_object_or_404(Timer, pk=kwargs['pk'], cycle=kwargs['cycle'], cycle__user=user)
		timer.down()

		return self.list(self, request, *args, **kwargs)

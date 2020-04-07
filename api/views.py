from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Activity, ActivityEvent
from .serializers import ActivityListSerializer, ActivityDetailSerializer, ActivityEventListSerializer, ActivityEventDetailSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Activity.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ActivityListSerializer
        else:
            return ActivityDetailSerializer

    def perform_create(self, serializer):
        user = self.request.user
        activity = serializer.save(user=user)

        ActivityEvent(
            activity=activity,
            date_time=timezone.now(),
            event_type=ActivityEvent.CREATED,
        ).save()

class ActivityEventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        activity = self.kwargs['activity']
        return ActivityEvent.objects.filter(activity=activity, activity__user=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ActivityEventListSerializer
        else:
            return ActivityEventDetailSerializer

    def perform_create(self, serializer):
        activity = self.kwargs['activity']
        serializer.save(activity=activity)
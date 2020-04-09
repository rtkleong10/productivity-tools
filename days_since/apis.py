from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from days_since.models import Activity, ActivityEvent
from days_since.serializers import ActivityListSerializer, ActivityDetailSerializer, ActivityEventListSerializer, ActivityEventDetailSerializer

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

class ActivityEventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        activity = get_object_or_404(Activity, pk=self.kwargs['activity'])
        return ActivityEvent.objects.filter(activity=activity, activity__user=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ActivityEventListSerializer
        else:
            return ActivityEventDetailSerializer

    def perform_create(self, serializer):
        activity = self.kwargs['activity']
        serializer.save(activity=Activity.objects.get(pk=activity))
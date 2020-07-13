from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import Activity, ActivityEvent
from .serializers import ActivityListSerializer, ActivityDetailSerializer, ActivityEventListSerializer, ActivityEventDetailSerializer, ActivityStatsSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    NUM_EVENTS_FOR_AVG_FREQ = 10
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
        serializer.save(user=user)

    @action(detail=True)
    def statistics(self, request, pk=None):
        activity = get_object_or_404(Activity, pk=pk)

        # Calculate average frequency
        recent_events = activity.events.order_by("-date")[:ActivityViewSet.NUM_EVENTS_FOR_AVG_FREQ]
        last_event = None
        total_diff = 0

        if len(recent_events) > 1:
            for event in recent_events:
                if last_event != None:
                    total_diff += (last_event.date - event.date).days

                last_event = event

            average_frequency = total_diff / (len(recent_events) - 1)

        else:
            average_frequency = None

        serializer = ActivityStatsSerializer(data={
            "total_count": activity.events.count(),
            "skipped_count": activity.events.filter(event_type=ActivityEvent.SKIPPED).count(),
            "completed_count": activity.events.filter(event_type=ActivityEvent.COMPLETED).count(),
            "average_frequency": average_frequency,
        })
        serializer.is_valid()

        return Response(serializer.data)

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
        date = serializer.validated_data.get("date")

        other_combi = self.get_queryset().filter(activity=activity, date=date).first()

        if other_combi:
            raise ValidationError(detail={
                api_settings.NON_FIELD_ERRORS_KEY: ["The fields activity, date must make a unique set."]
            })

        serializer.save(activity=Activity.objects.get(pk=activity))

    def perform_update(self, serializer):
        pk = serializer.instance.pk
        activity = serializer.instance.activity
        date = serializer.validated_data.get("date")

        other_combi = self.get_queryset().filter(activity=activity, date=date).exclude(pk=pk).first()

        if other_combi:
            raise ValidationError(detail={
                api_settings.NON_FIELD_ERRORS_KEY: ["The fields activity, date must make a unique set."]
            })

        serializer.save()

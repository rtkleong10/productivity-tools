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
    """
    An activity contain events which are when you perform that activity. Activities allow you to keep track of these related events and note how long it's been since the last event.

    # Fields
    - Title
    - Description
    - Frequency (in days) (optional)
    - Color (color refers to the id of the color in the colors list)

    ## Additional Readonly Fields
    - Today's event: The event type of today's event, if applicable (refer to the Event List for what each type stands for)
    - Last event type: The event type of the most recent event (refer to the Event List for what each type stands for)
    - Days since: Days since the last event or since creation if there's no events recorded

    # Statistics
    - To get the statistics of a particular activity, go the activity page and use the extra action (Statistics)

    ## Contains
    - Total count
    - Skipped count
    - Completed count
    - Average frequency (over the last 10 events)
        - `null` if < 2 events recorded
    """
    NUM_EVENTS_FOR_AVG_FREQ = 10
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Activity.objects.filter(user=user).order_by('frequency')

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
        user = request.user
        activity = get_object_or_404(Activity, pk=pk, user=user)

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
    """
    An event is an instance of performing an activity. Events are linked to a date, so only 1 event can be performed per day per activity.

    # Fields
    - Date
    - Event type
    - Description

    ## Event Types
    - 1: Completed
    - 2: Skipped
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        activity = get_object_or_404(Activity, pk=self.kwargs['activity'], user=user)
        return ActivityEvent.objects.filter(activity=activity).order_by("-date")

    def get_serializer_class(self):
        if self.action == 'list':
            return ActivityEventListSerializer
        else:
            return ActivityEventDetailSerializer

    def perform_create(self, serializer):
        user = self.request.user
        activity_pk = self.kwargs['activity']
        get_object_or_404(Activity, pk=activity_pk, user=user)

        date = serializer.validated_data.get("date")
        other_combi = self.get_queryset().filter(activity=activity_pk, date=date).first()

        if other_combi:
            raise ValidationError(detail={
                api_settings.NON_FIELD_ERRORS_KEY: ["The fields activity, date must make a unique set."]
            })

        serializer.save(activity=Activity.objects.get(pk=activity_pk))

    def perform_update(self, serializer):
        user = self.request.user
        pk = serializer.instance.pk
        get_object_or_404(ActivityEvent, pk=pk, activity__user=user)

        activity_pk = serializer.instance.activity
        date = serializer.validated_data.get("date")

        other_combi = self.get_queryset().filter(activity=activity_pk, date=date).exclude(pk=pk).first()

        if other_combi:
            raise ValidationError(detail={
                api_settings.NON_FIELD_ERRORS_KEY: ["The fields activity, date must make a unique set."]
            })

        serializer.save()

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from .models import Activity, ActivityEvent
from .serializers import ActivityListSerializer, ActivityDetailSerializer, ActivityEventListSerializer, ActivityEventDetailSerializer
from rest_framework.exceptions import ValidationError

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
        serializer.save(user=user)

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

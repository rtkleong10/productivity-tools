from rest_framework import serializers
from .models import Activity, ActivityEvent
from utils.serializers import ParameterisedHyperlinkedIdentityField

class ActivityListSerializer(serializers.HyperlinkedModelSerializer):
    color = serializers.IntegerField(source="color.pk")

    class Meta:
        model = Activity
        fields = (
            'id',
            'url',
            'title',
            'frequency',
            'last_event_type',
            'days_since',
            'todays_event',
            'color',
        )

class ActivityDetailSerializer(serializers.ModelSerializer):
    events = ParameterisedHyperlinkedIdentityField(
        view_name='common:activityevent-list',
        lookup_fields=(('pk', 'activity'),),
    )

    class Meta:
        model = Activity
        exclude = ('user',)

class ActivityEventListSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(
        view_name='common:activityevent-detail',
        lookup_fields=(('activity.pk', 'activity'), ('pk', 'pk'))
    )

    class Meta:
        model = ActivityEvent
        fields = '__all__'
        read_only_fields = ('activity',)

class ActivityEventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityEvent
        fields = '__all__'
        read_only_fields = ('activity',)

class ActivityStatsSerializer(serializers.Serializer):
    total_count = serializers.IntegerField(min_value=0)
    skipped_count = serializers.IntegerField(min_value=0)
    completed_count = serializers.IntegerField(min_value=0)
    average_frequency = serializers.FloatField()


from rest_framework import serializers
from .models import Activity, ActivityEvent
from utils.serializers import ParameterisedHyperlinkedIdentityField

class ActivityListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'id',
            'url',
            'title',
            'frequency',
            'is_frequency_exceeded',
            'days_since',
        )

class ActivityDetailSerializer(serializers.ModelSerializer):
    events = ParameterisedHyperlinkedIdentityField(
        view_name='api:activityevent-list',
        lookup_fields=(('pk', 'activity'),),
    )

    class Meta:
        model = Activity
        exclude = ('user',)

class ActivityEventListSerializer(serializers.ModelSerializer):
    url = ParameterisedHyperlinkedIdentityField(
        view_name='api:activityevent-detail',
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
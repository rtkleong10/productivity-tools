from rest_framework import serializers
from .models import Cycle, Timer
from utils.serializers import ParameterisedHyperlinkedIdentityField

class CycleListSerializer(serializers.HyperlinkedModelSerializer):
	total_duration = serializers.DurationField()

	class Meta:
		model = Cycle
		fields = (
			'id',
			'url',
			'title',
			'total_duration',
		)


class CycleDetailSerializer(serializers.ModelSerializer):
	timers = ParameterisedHyperlinkedIdentityField(
		view_name='common:timer-list',
		lookup_fields=(('pk', 'cycle'),),
	)

	class Meta:
		model = Cycle
		exclude = ('user',)

class TimerListSerializer(serializers.ModelSerializer):
	url = ParameterisedHyperlinkedIdentityField(
		view_name='common:timer-detail',
		lookup_fields=(('cycle.pk', 'cycle'), ('pk', 'pk'))
	)

	class Meta:
		model = Timer
		fields = '__all__'
		read_only_fields = ('cycle',)

class TimerDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Timer
		fields = '__all__'
		read_only_fields = ('cycle',)

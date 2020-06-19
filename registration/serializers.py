from rest_framework import serializers
from .models import UserProfile

class ProfileSerializer(serializers.ModelSerializer):
    timezone = serializers.CharField()

    class Meta:
        model = UserProfile
        exclude = (
            'id',
            'user',
        )

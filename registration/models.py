from django.db import models
from django.conf import settings
from timezone_field import TimeZoneField

class UserProfile(models.Model):
    user = models.OneToOneField(
        help_text='The user to which the profile belongs to.',
        to=settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    timezone = TimeZoneField(
        help_text='The timezone to use as reference',
        default='Asia/Singapore',
    )

    def __str__(self):
        return self.user.username
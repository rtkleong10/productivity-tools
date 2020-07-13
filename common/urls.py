from django.urls import path, include
from .apis import ColorViewSet, TimezoneViewSet, DefaultRouterWithSimpleViews
from days_since.apis import ActivityViewSet, ActivityEventViewSet
from registration.apis import ProfileView

router = DefaultRouterWithSimpleViews()
router.register(r'colors', ColorViewSet, basename='colors')
router.register(r'timezones', TimezoneViewSet, basename='timezones')
router.register(r'profile', ProfileView, basename='profile')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'activities/(?P<activity>[^/.]+)/events', ActivityEventViewSet, basename='activityevent')

urlpatterns = [
    path('', include((router.urls, 'api'), namespace='api')),
]

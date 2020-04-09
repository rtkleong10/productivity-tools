from django.urls import path, include
from rest_framework.routers import DefaultRouter
from days_since.apis import ActivityViewSet, ActivityEventViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'activities/(?P<activity>[^/.]+)/events', ActivityEventViewSet, basename='activityevent')

urlpatterns = [
    path('', include((router.urls, 'api'), namespace='api')),
]

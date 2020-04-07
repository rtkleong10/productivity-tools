from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ActivityEventViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'activities/(?P<activity>[^/.]+)/events', ActivityEventViewSet, basename='activityevent')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include((router.urls, 'api'), namespace='api')),
]
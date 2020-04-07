# from .views import ActivityViewSet
# from django.urls import path
# from rest_framework import routers
# from rest_framework.urlpatterns import format_suffix_patterns
#
# urlpatterns = format_suffix_patterns([
# 	path("activities/", ActivityViewSet.as_view(
# 		actions={
# 			"get": "list",
# 			"post": "create",
# 		},
# 	), name="activity-list"),
#
# 	path("activities/<int:pk>/", ActivityViewSet.as_view(
# 		actions={
# 			"get": "retrieve",
# 			"put": "update",
# 			"patch": "update",
# 			"delete": "destroy",
# 		},
# 	), name="activity-detail"),
# 	path('activities/<int:pk>/events/', ActivityViewSet.as_view(
# 		actions={
# 			'get': "events"
# 		},
# 	), name='activityevent-list')
# ])

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ActivityEventViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'activities/(?P<activity>[^/.]+)/events', ActivityEventViewSet, basename='activityevent')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
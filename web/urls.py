from django.urls import path
from .views import *

app_name = 'web'
urlpatterns = [
	path('', home_view, name='home'),
	path('activities/create/', CreateActivity.as_view(), name='create-activity'),
	path('activities/<uuid:pk>/edit', UpdateActivity.as_view(), name='update-activity'),
	path('activities/<uuid:pk>/delete', DeleteActivity.as_view(), name='delete-activity'),
	path('activities/<uuid:activity>/events/create/', CreateEvent.as_view(), name='create-event'),
	path('events/<uuid:pk>/edit', UpdateEvent.as_view(), name='update-event'),
	path('events/<uuid:pk>/delete', DeleteEvent.as_view(), name='delete-event'),
	path('activities/<uuid:pk>/details', activity_detail, name='activity-detail'),
	path('activities/<uuid:pk>/complete/', complete_activity, name='complete-activity'),
	path('activities/<uuid:pk>/skip/', skip_activity, name='skip-activity'),
]
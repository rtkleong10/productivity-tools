from django.urls import path, include
from utils.routers import  DefaultRouterWithSimpleViews
from .apis import ColorListView, TimezoneListView, HomeView
from days_since.apis import ActivityViewSet, ActivityEventViewSet
from time_cycles.apis import CycleViewSet, TimerViewSet

router = DefaultRouterWithSimpleViews()
router.register(r'colors', ColorListView, basename='colors')
router.register(r'timezones', TimezoneListView, basename='timezones')

# Days Since
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'activities/(?P<activity>[^/.]+)/events', ActivityEventViewSet, basename='activityevent')

# Time Cycles
router.register(r'cycles', CycleViewSet, basename='cycle')
router.register(r'cycles/(?P<cycle>[^/.]+)/timers', TimerViewSet, basename='timer')

app_name = 'common'
urlpatterns = [
    path('api/', include(router.urls)),
    path('', HomeView.as_view(), name='home'),
]

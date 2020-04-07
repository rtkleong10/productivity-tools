from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, ActivityEventViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'activities/(?P<activity>[^/.]+)/events', ActivityEventViewSet, basename='activityevent')

urlpatterns = router.urls
from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from utils.routers import  DefaultRouterWithSimpleViews
from .apis import ProfileView, LoginView, LogoutView

router = DefaultRouterWithSimpleViews(title="Auth Root")

router.register(r'users', UserViewSet, basename='users')
router.register(r'jwt/create', TokenObtainPairView, basename='jwt-create')
router.register(r'jwt/refresh', TokenRefreshView, basename='jwt-refresh')

router.register(r'profile', ProfileView, basename='profile')
router.register(r'login', LoginView, basename='login')
router.register(r'logout', LogoutView, basename='logout')

app_name = 'registration'
urlpatterns = [
	path('', include(router.urls)),
]

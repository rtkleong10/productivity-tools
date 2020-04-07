from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import signup_view, logout_view, ProfileView

app_name = 'registration'
urlpatterns = [
	path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('signup/', signup_view, name='signup'),
	path('logout/', logout_view, name='logout'),
	path('profile/', ProfileView.as_view(), name='profile'),
]
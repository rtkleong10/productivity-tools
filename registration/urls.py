from django.urls import path, include

app_name = 'registration'
urlpatterns = [
	path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
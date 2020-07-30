"""productivity_tools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

admin.site.site_header = "Productivity Tools Admin Panel"
admin.site.site_title = "Productivity Tools Admin Panel"
admin.site.index_title = "Welcome to the Productivity Tools Admin Panel"

favicon_view = RedirectView.as_view(url='/static/images/favicon/favicon.ico', permanent=True)

urlpatterns = [
    path('favicon.ico/', favicon_view),
    path('auth/', include('registration.urls')),
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
]

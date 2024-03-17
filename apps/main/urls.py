"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import MainHomeView

app_name = "main"

if settings.DEBUG:
    # show an uncached version of the home page
    base_path = MainHomeView.as_view()
else:
    # cache the home page in production
    twelve_hours: int = 60 * 60 * 12
    base_path = cache_page(twelve_hours)(MainHomeView.as_view())

urlpatterns = [
    path("", base_path, name="index"),
]

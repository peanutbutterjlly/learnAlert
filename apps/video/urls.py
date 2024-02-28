from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import video_list

app_name = "video"

if settings.DEBUG:
    base_path = video_list
else:
    twelve_hours = 60 * 60 * 12
    base_path = cache_page(twelve_hours)(video_list)

urlpatterns = [
    path("", base_path, name="list"),
]

from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostDetailView, blog_list

app_name = "blog"

if settings.DEBUG:
    base_path = blog_list
else:
    twelve_hours = 60 * 60 * 12
    base_path = cache_page(twelve_hours)(blog_list)

urlpatterns = [
    path("", base_path, name="list"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail"),
]

from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    PostDetailView,
    blog_list,
    react_to_post,
)

app_name = "blog"

if settings.DEBUG:
    base_path = blog_list
else:
    twelve_hours = 60 * 60 * 12
    base_path = cache_page(twelve_hours)(blog_list)

urlpatterns = [
    path("", base_path, name="list"),
    path("<slug:slug>/", PostDetailView.as_view(), name="detail"),
    path("react/<slug:slug>/<str:reaction>/", react_to_post, name="react_to_post"),
]

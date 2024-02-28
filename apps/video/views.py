from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Video


@require_GET
def video_list(request: HttpRequest) -> HttpResponse:
    """checks the headers to determine if the request is HTMX or not then
    renders a listing of all videos"""
    videos: list[Video] = Video.objects.all()

    if request.htmx:
        template_name = "partials/_video_list.html"
    else:
        template_name = "video/videos.html"

    return render(request, template_name, {"videos": videos})

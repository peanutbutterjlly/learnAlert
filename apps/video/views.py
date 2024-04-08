from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Video


@require_GET
def video_list(request: HttpRequest) -> HttpResponse:
    """renders a listing of all videos"""
    videos: list[Video] = Video.objects.all()

    template_name = "video/videos.html"

    return render(request, template_name, {"videos": videos})

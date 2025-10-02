from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Video


@require_GET
def video_list(request: HttpRequest) -> HttpResponse:
    """renders a listing of all videos"""
    paginated_videos = Paginator(Video.objects.all().order_by("-retrieved_at"), 12)
    page_number = request.GET.get("page")
    page_obj = paginated_videos.get_page(page_number)

    template_name = "video/videos.html"

    context = {
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
        "videos": page_obj,
    }

    return render(request, template_name, context)

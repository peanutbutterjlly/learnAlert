from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView

from apps.blog.models import Post
from apps.video.models import Video


class MainHomeView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        """add the 3 most recent blog posts and videos to the context"""
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()[:3]
        context["videos"] = Video.objects.all()[:3]
        return context


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


@require_GET
def blog_list(request: HttpRequest) -> HttpResponse:
    posts: list[Post] = Post.objects.all()

    if request.htmx:
        template_name = "partials/_post_list.html"
    else:
        template_name = "main/index.html"

    return render(request, template_name, {"posts": posts})

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.generic import DetailView

from .models import Post


@require_GET
def blog_list(request: HttpRequest) -> HttpResponse:
    posts: list[Post] = Post.objects.all()

    if request.htmx:
        template_name = "partials/_post_list.html"
    else:
        template_name = "blog/posts.html"

    return render(request, template_name, {"posts": posts})


class PostDetailView(DetailView):
    context_object_name: str = "post"
    model = Post
    template_name: str = "blog/detail.html"

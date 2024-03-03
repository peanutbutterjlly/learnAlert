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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_post"] = Post.objects.filter(id__gt=self.object.id).first()
        context["previous_post"] = Post.objects.filter(id__lt=self.object.id).last()
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        post = self.get_object()
        if "like" in request.POST:
            post.likes += 1
            post.save()
            if request.htmx:
                return HttpResponse(f"Likes: {post.likes}")
        return super().post(request, *args, **kwargs)

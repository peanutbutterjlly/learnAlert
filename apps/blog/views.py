from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
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

    def get_context_data(self, **kwargs) -> dict:
        reactions = [
            ("like", "👍", self.object.likes),
            ("dislike", "💩", self.object.dislikes),
            ("shock", "😱", self.object.shocks),
            ("eye", "👀", self.object.eyes),
        ]

        context = super().get_context_data(**kwargs)
        context["next_post"] = Post.objects.filter(id__gt=self.object.id).first()
        context["previous_post"] = Post.objects.filter(id__lt=self.object.id).last()
        context["reactions"] = reactions
        return context


@require_POST
def like_post(request: HttpRequest, slug: str) -> HttpResponse:
    print("liking post")
    post = Post.objects.get(slug=slug)
    post.likes += 1
    post.save()
    return HttpResponse(f"Likes: {post.likes}")


@require_POST
def dislike_post(request: HttpRequest, slug: str) -> HttpResponse:
    post = Post.objects.get(slug=slug)
    post.dislikes += 1
    post.save()
    return HttpResponse(f"Dislikes: {post.dislikes}")


@require_POST
def shock_post(request: HttpRequest, slug: str) -> HttpResponse:
    post = Post.objects.get(slug=slug)
    post.shocks += 1
    post.save()
    return HttpResponse(f"Shocks: {post.shocks}")


@require_POST
def eye_post(request: HttpRequest, slug: str) -> HttpResponse:
    post = Post.objects.get(slug=slug)
    post.eyes += 1
    post.save()
    return HttpResponse(f"Eyes: {post.eyes}")


@require_POST
def react_to_post(request: HttpRequest, slug: str, reaction: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=slug)

    updated_count = 0

    if reaction == "like":
        post.likes += 1
        updated_count = post.likes
    elif reaction == "dislike":
        post.dislikes += 1
        updated_count = post.dislikes
    elif reaction == "shock":
        post.shocks += 1
        updated_count = post.shocks
    elif reaction == "eye":
        post.eyes += 1
        updated_count = post.eyes
    post.save()

    return HttpResponse(f"{updated_count}")

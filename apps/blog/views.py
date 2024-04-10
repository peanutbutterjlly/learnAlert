from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import DetailView

from .models import Post


@require_GET
def blog_list(request: HttpRequest) -> HttpResponse:
    """renders a listing of all blog posts"""
    posts: list[Post] = Post.published.all()

    template_name = "blog/posts.html"

    return render(request, template_name, {"posts": posts})


class PostDetailView(DetailView):
    """renders a single blog post with reactions, next, and previous posts"""

    context_object_name: str = "post"
    model = Post
    template_name: str = "blog/detail.html"

    def get_context_data(self, **kwargs) -> dict:
        """add reactions & next and previous posts to the context"""
        context = super().get_context_data(**kwargs)
        post: Post = self.get_object()
        reactions = [
            ("like", "👍", self.object.likes, "I (somehow) like it"),
            ("dislike", "💩", self.object.dislikes, "This sucks!"),
            ("shock", "😱", self.object.shocks, "Unbelievable."),
            ("robot", "🤖️", self.object.robots, "Only a robot could've wrote this!"),
        ]
        context["next_post"] = post.next_post
        context["previous_post"] = post.previous_post
        context["reactions"] = reactions
        return context


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
    elif reaction == "robot":
        post.robots += 1
        updated_count = post.robots
    post.save()

    return HttpResponse(f"{updated_count}")

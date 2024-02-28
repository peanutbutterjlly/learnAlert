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

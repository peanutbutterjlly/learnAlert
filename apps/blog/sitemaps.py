from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def location(self, item):
        return reverse("blog:detail", args=[item.slug])

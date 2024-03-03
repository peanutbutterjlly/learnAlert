from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from apps.blog.models import Post


class RssFeeds(Feed):
    title = "Steve's Blog"
    link = "/blog/"
    description = "The latest blog posts from Steve"

    def items(self):
        return Post.objects.order_by("-published_date")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)

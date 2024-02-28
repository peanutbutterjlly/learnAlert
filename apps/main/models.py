from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    content = models.TextField()
    author_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    blog_post = models.ForeignKey(
        "blog.BlogPost",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )
    video = models.ForeignKey(
        "video.Video",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.content[:20]

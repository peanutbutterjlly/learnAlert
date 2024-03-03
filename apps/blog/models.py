from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.main.models import Category


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    author = models.CharField(max_length=50, default="Steve Rios")
    description = models.TextField(max_length=255, blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    likes = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self) -> str:
        # you have to namespace the url in the path function and provide it the name of 'detail'
        return reverse("blog:detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ["-published_date"]
        indexes = [
            models.Index(fields=["-published_date"]),
        ]

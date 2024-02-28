from django.db import models
from django.urls import reverse

from apps.main.models import Category


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    author = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True, null=True)
    published_date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self) -> str:
        # you have to namespace the url in the path function and provide it the name of 'detail'
        return reverse("blog:detail", args=[self.id])  # type: ignore

    class Meta:
        ordering = ["-published_date"]

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"{self.title} by {self.author}"

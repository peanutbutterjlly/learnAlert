from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.main.models import Category


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=150)
    content = models.TextField()
    author = models.CharField(max_length=50, default="Steve Rios")
    description = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    shocks = models.PositiveIntegerField(default=0)
    robots = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=200)

    objects = models.Manager()
    published = PublishedManager()

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

    @property
    def next_post(self):
        """Returns the next published post based on published_date."""
        return (
            Post.published.filter(published_date__gt=self.published_date)
            .order_by("published_date")
            .first()
        )

    @property
    def previous_post(self):
        """Returns the previous published post based on published_date."""
        return (
            Post.published.filter(published_date__lt=self.published_date)
            .order_by("-published_date")
            .first()
        )

    class Meta:
        ordering = ["-published_date"]
        indexes = [
            models.Index(fields=["-published_date"]),
        ]

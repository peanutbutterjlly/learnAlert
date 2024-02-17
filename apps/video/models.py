from django.db import models
from django.urls import reverse
from apps.main.models import Category


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, null=True)
    vid_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    retrieved_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="videos", null=True
    )

    def get_absolute_url(self) -> str:
        # you have to namespace the url in the path function and provide it the name of 'detail'
        return reverse("videos:detail", args=[self.id])  # type: ignore

    def __str__(self) -> str:
        """Return a truncated version of the title if its length is greater than 20 characters, otherwise return the title itself."""
        return f"{self.title[:20]}..." if len(self.title) > 20 else self.title

    class Meta:
        """defines the ordering of the videos"""

        ordering: list = ["-retrieved_at"]

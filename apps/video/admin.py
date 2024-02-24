from django.contrib import admin

from apps.video.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass

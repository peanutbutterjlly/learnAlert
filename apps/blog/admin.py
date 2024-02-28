from django.contrib import admin

from apps.blog.models import BlogPost as Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

from django import forms
from django.contrib import admin
from django.db import models

from apps.blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ("likes", "dislikes", "shocks", "eyes")
    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"rows": 20, "cols": 100})},
        models.CharField: {"widget": forms.TextInput(attrs={"size": 100})},
    }

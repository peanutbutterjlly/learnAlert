# Generated by Django 5.0.2 on 2024-03-10 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0008_post_blog_post_publish_a3f863_idx"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="dislikes",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="post",
            name="eyes",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="post",
            name="shocks",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
# Generated by Django 5.0.2 on 2024-03-03 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0007_post_slug"),
        ("main", "0003_alter_category_options"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["-published_date"], name="blog_post_publish_a3f863_idx"
            ),
        ),
    ]

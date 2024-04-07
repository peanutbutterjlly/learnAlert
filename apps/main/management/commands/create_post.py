# this will be for hitting the ANTHROPIC_API for claude to write me blog posts
import anthropic
from decouple import config
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Bot that will create posts from the ANTHROPIC_API to be stored in the database."

    def __init__(self, *args, **kwargs) -> None:
        """initialize the ANTHROPIC_API service"""
        super().__init__(*args, **kwargs)
        self.api_key: str = config("ANTHROPIC_API_KEY", cast=str)
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def get_blog_posts(self) -> list[dict]:
        """create a blog post from the ANTHROPIC_API"""

        message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            temperature=0.5,
            system="Write engaging, SEO-optimized blog posts on web dev, Python, & JavaScript,\
                   focusing on trends & best practices for developers & enthusiasts.",
        )

        print(message)

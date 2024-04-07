from datetime import datetime
from random import choice

import anthropic
from anthropic.types.message import Message
from decouple import config
from django.core.management.base import BaseCommand

from apps.blog.models import Post
from apps.main.models import Category


class Command(BaseCommand):
    help = "Bot that will create posts from the ANTHROPIC_API to be stored in the database."

    def __init__(self, *args, **kwargs) -> None:
        """initialize the ANTHROPIC_API service"""
        super().__init__(*args, **kwargs)
        self.api_key: str = config("ANTHROPIC_API_KEY", cast=str)
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def get_topic(self) -> str:
        """create a topic from the ANTHROPIC_API"""

        CURRENT_YEAR: str = str(datetime.now().year)

        subjects = (
            "Beginner's Guide to",
            "The Future of",
            "The Rise of",
            "Mastering",
            "Understanding",
            "The Secrets of",
            "Exploring",
            "The Evolution of",
        )
        adjectives = (
            "Advanced",
            "Practical",
            "Innovative",
            "Essential",
            "Comprehensive",
            "Simplified",
            "Interactive",
            "Cutting-Edge",
        )
        technologies = (
            "React.js",
            "CSS Grid Layouts",
            "CSS Flexbox",
            "Node.js",
            "Django",
            "Flask",
            "FastAPI",
            "Python",
            "Pypy",
            "Python Web Frameworks",
            "Python Type Hints",
            "Vue.js Composition API",
            "Kubernetes for DevOps",
            "Machine Learning with TensorFlow",
            "SvelteKit and Sapper",
            "NestJS",
            "Deno JS",
            "Express.js",
            "Next.js",
            "Docker for DevOps",
            "AWS for DevOps",
            "Azure",
            "Firebase",
            "Bun JS runtime",
            "Vite",
            "Nuxt.js",
            "Svelte",
            "SvelteKit",
            "Vanilla JavaScript",
            "TypeScript",
            "Tailwind CSS",
            "WordPress",
            "React Native",
        )
        trends = (
            f"in {CURRENT_YEAR}",
            "for Big Data",
            "in the Cloud Computing Space",
            "for Mobile Development",
            "in Web Security",
            "for Startups",
            "in AI Development",
            "in Open Source Projects",
            "in Web Development",
            "for Data Science",
            "in Cloud Computing",
        )
        skills_concepts = (
            "Best Practices",
            "Tips and Tricks",
            "Core Concepts",
            "Design Patterns",
            "Performance Optimization Techniques",
            "Security Vulnerabilities to Avoid",
            "Debugging Strategies",
            "Project Management Fundamentals",
        )

        subject = choice(subjects)
        adjective = choice(adjectives)
        technology = choice(technologies)
        trend = choice(trends)
        skill_concept = choice(skills_concepts)

        # Mix and match for more variety
        patterns = (
            f"{subject} {adjective} {technology} {trend}",
            f"{adjective} {skill_concept} {technology}",
            f"{technology}: {subject} {skill_concept}",
            f"{subject} {technology} {trend}",
            f"{technology} {trend}: {adjective} {skill_concept}",
        )

        blog_topic = choice(patterns)

        print(f"Blog topic: {blog_topic}")
        return blog_topic

    def get_title(self, topic: str) -> str:
        """create a title from the ANTHROPIC_API"""

        title_request: Message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            temperature=0.5,
            stream=False,
            system="Craft a catchy, SEO-optimized title for a blog post on the latest web dev, Python,\
                    CSS, & JavaScript trends for developers & tech enthusiasts.",
            messages=[
                {
                    "role": "user",
                    "content": f"Create a title for a blog post on {topic}; only return the title\
                     itself, no other accompanying text, or even quotation marks",
                }
            ],
        )

        title = title_request.dict()["content"][0]["text"]
        print(f"Blog title: {title}")
        return title

    def get_meta_keywords(self, title: str) -> str:
        """generate meta keywords for a blog post from the based on the title passed in"""

        KEYWORDS_PROMPT = f"""
            Generate SEO-friendly meta keywords for a blog post titled "{title}" on web development, Python, and JavaScript trends.
            return only the keywords only, comma separated
        """

        meta_keywords_request: Message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            temperature=0.5,
            stream=False,
            system="You're an engaging tech blog-post writer who writes SEO-optimized blog posts on web dev,\
                    Python, CSS, or JavaScript, focusing on trends & best practices for developers & enthusiasts.",
            messages=[
                {
                    "role": "user",
                    "content": KEYWORDS_PROMPT.format(title=title),
                }
            ],
        )

        keywords = meta_keywords_request.dict()["content"][0]["text"]
        print(f"Meta keywords: {keywords}")
        return keywords

    def get_description(self, title: str) -> str:
        DESCRIPTION_PROMPT = f"""
            Describe a blog-post in roughly 240 characters based on this title: "{title}". return only the description text
        """

        description_request: Message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=777,
            temperature=0.5,
            stream=False,
            system="You're an engaging blog post writer who writes SEO-optimized blog posts on web dev,\
                    Python, CSS, or JavaScript, focusing on trends & best practices for developers & enthusiasts.",
            messages=[
                {
                    "role": "user",
                    "content": DESCRIPTION_PROMPT.format(title=title),
                }
            ],
        )

        description = description_request.dict()["content"][0]["text"]
        print(f"Description: {description}")
        return description

    def create_blog_post(self) -> list[dict]:
        """create a blog post from the ANTHROPIC_API"""

        TOPIC: str = self.get_topic()
        TITLE: str = self.get_title(TOPIC)
        META_KEYWORDS: str = self.get_meta_keywords(TITLE)
        DESCRIPTION: str = self.get_description(TITLE)

        CONTENT_PROMPT = """
            Write a complete blog post based on the following title: '{TITLE}'; return the content in
            markdown format - no need to return the title again, or any accompanying text like 
            "here is a blog post..."; just provide a complete blog post. when returning the content,
            please DO NOT put the title as the initial header, since I already have it, I'll insert
            it myself. DO NOT TELL ME " here is the blog post..." - just return me blog content
        """

        content_request: Message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4000,
            temperature=0.5,
            stream=False,
            system="Write engaging, SEO-optimized blog posts on web dev, Python, CSS, or JavaScript,\
                   focusing on trends & best practices for developers & enthusiasts.",
            messages=[
                {
                    "role": "user",
                    "content": CONTENT_PROMPT.format(TITLE=TITLE),
                }
            ],
        )

        blog_content = content_request.dict()["content"][0]["text"]
        return TITLE, META_KEYWORDS, DESCRIPTION, blog_content

    def determine_category(self, title: str, content: str) -> str:
        CATEGORY_KEYWORDS = {
            "Javascript": [
                "Javascript",
                "JS ",
                "Node.js",
                "React",
                "Vue.js",
                "Angular",
                "TypeScript",
            ],
            "Django": ["Django", "Python web framework"],
            "Python": ["Python", "Flask", "PyTorch", "Pandas", "Machine Learning", "Data Science"],
            "CSS": ["CSS", "Flexbox", "Grid", "Animations", "Responsive Design"],
            "Web Development": [
                "Web Development",
                "Web Design",
                "HTML",
                "Frontend",
                "Backend",
                "Fullstack",
            ],
        }
        category_scores = {category: 0 for category in CATEGORY_KEYWORDS}

        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in title.lower() or keyword.lower() in content.lower():
                    category_scores[category] += 1

        # Determine the category with the highest score
        max_category = max(category_scores, key=category_scores.get)

        # If no keywords matched, default to 'Web Development'
        if category_scores[max_category] == 0:
            print("No keywords matched, defaulting to 'Web Development'")
            return "Web Development"

        print(f"Category: {max_category}")
        return max_category

    def handle(self, *args, **kwargs):
        """get topic, title, keywords, description, and content and post it in the Post model database"""
        TITLE, META_KEYWORDS, DESCRIPTION, blog_content = self.create_blog_post()

        # publish it immediately and hope it doesn't have shitty content
        STATUS = Post.Status.PUBLISHED

        category_name = self.determine_category(TITLE, blog_content)
        category, created = Category.objects.get_or_create(name=category_name)

        Post.objects.create(
            title=TITLE,
            meta_keywords=META_KEYWORDS,
            description=DESCRIPTION,
            content=blog_content,
            status=STATUS,
            category=category,
        )

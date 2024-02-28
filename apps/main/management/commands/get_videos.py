from decouple import config
from django.core.management.base import BaseCommand
from googleapiclient.discovery import build

from apps.main.models import Category
from apps.video.models import Video

# video model, for reference
# class Video(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.CharField(max_length=500, blank=True, null=True)
#     vid_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
#     retrieved_at = models.DateTimeField(auto_now_add=True)
#     category = models.ForeignKey(
#         Category, on_delete=models.SET_NULL, related_name="videos", null=True
#     )


class Command(BaseCommand):
    help = "Bot that will get the videos from the YouTube API to be stored in the database."

    def __init__(self, *args, **kwargs) -> None:
        """initialize the YouTube API service"""
        super().__init__(*args, **kwargs)
        self.api_key: str = config("YOUTUBE_API_KEY")
        self.youtube_service = build("youtube", "v3", developerKey=self.api_key)

    def get_videos(self) -> list[dict]:
        """get programming related videos from the YouTube API"""

        MAX_RESULTS = 5
        # the total number of videos you'll be getting is MAX_RESULTS * len(QUERIES)
        QUERIES = {
            "javascript web development tips and tricks": "Javascript",
            "django python programming": "Django",
            "css programming tips and tricks": "CSS",
        }

        search_results_for_video_ids: list[dict] = []
        video_id_to_category: dict = {}

        # this first query is to get a list of video ids
        for query, category_name in QUERIES.items():
            search_params = {
                "part": "snippet",
                "maxResults": MAX_RESULTS,
                "order": "relevance",
                "q": query,
                "safeSearch": "strict",
                "type": "video",
                "videoDuration": "medium",
                "videoEmbeddable": "true",
                "videoSyndicated": "true",  # can be played outside of YouTube
            }

            search_response: dict = (
                self.youtube_service.search().list(**search_params).execute()
            )
            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                video_id_to_category[video_id] = category_name
                search_results_for_video_ids.append(item)

        video_ids = [item["id"]["videoId"] for item in search_results_for_video_ids]

        # now that we have the video ids, we need to get the details of each video
        video_params = {
            "part": "snippet",
            "id": ",".join(video_ids),
            "maxResults": MAX_RESULTS,
        }

        # Call the videos.list method to retrieve location details for each video.
        video_response: dict = (
            self.youtube_service.videos().list(**video_params).execute()
        )

        # set to keep track of the video titles already added
        already_added: set = set()
        # list to store cleaned videos
        cleaned_video_results: list[dict] = []

        for video in video_response.get("items", []):
            if video["id"] not in already_added:
                cleaned_video_results.append(
                    {
                        "description": video["snippet"]["description"],
                        "title": video["snippet"]["title"],
                        "vid_id": video.get("id"),
                        "category_name": video_id_to_category.get(
                            video["id"], "General"
                        ),
                    }
                )
                already_added.add(video["id"])

        return cleaned_video_results

    def insert_videos(self, videos: list[dict]) -> None:
        for video in videos:
            category_name = video.pop("category_name")
            category, created = Category.objects.get_or_create(name=category_name)

            video_obj, created = Video.objects.get_or_create(
                vid_id=video["vid_id"],
                defaults={
                    "title": video["title"],
                    "description": video["description"],
                    "category": category,
                },
            )
            if created:
                self.stdout.write(f"Successfully inserted video: {video_obj.title}")
            else:
                self.stdout.write(f"Video already exists: {video_obj.title}")

    def handle(self, *args, **kwargs) -> None:
        self.stdout.write("Running scraper")
        videos = self.get_videos()
        self.insert_videos(videos)

from typing import List
import time
import logging

class SocialChannel:
    def __init__(self, followers: int):
        self.followers = followers

    def post_message(self, message: str) -> None:
        raise NotImplementedError("Subclasses must implement this method.")


class YouTubeChannel(SocialChannel):
    def post_message(self, message: str) -> None:
        logging.info(f"Posting to YouTube: {message}")

class FacebookChannel(SocialChannel):
    def post_message(self, message: str) -> None:
        logging.info(f"Posting to Facebook: {message}")

class TwitterChannel(SocialChannel):
    def post_message(self, message: str) -> None:
        logging.info(f"Posting to Twitter: {message}")

class Post:
    def __init__(self, message: str, timestamp: int):
        self.message = message
        self.timestamp = timestamp

def process_schedule(posts: List[Post], channels: List[SocialChannel]) -> None:
    for post in posts:
        if post.timestamp <= time.time():
            for channel in channels:
                channel.post_message(post.message)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    youtube = YouTubeChannel(followers=1000)
    facebook = FacebookChannel(followers=500)
    twitter = TwitterChannel(followers=800)

    posts = [
        Post(message="Hello, world!", timestamp=int(time.time())),
        Post(message="Another post", timestamp=int(time.time()) + 10),
    ]

    channels = [youtube, facebook, twitter]

    process_schedule(posts, channels)

# Content Creation Tool
# This script fetches local trending news, rewrites the article with OpenAI,
# generates images with DALL·E, compiles them into a short video watermarked
# with a QR code linking back to the article, and creates scripts for a podcast
# episode and YouTube short. Upload steps to YouTube, podcast hosting services
# and Wordpress remain placeholders.
#
# Note: Actual network calls and authentication are not implemented.

from dataclasses import dataclass
import requests
from typing import Optional, List

import openai
import qrcode
from moviepy.editor import ImageClip, CompositeVideoClip, concatenate_videoclips

@dataclass
class NewsArticle:
    title: str
    content: str
    url: str


def fetch_local_trending_news(location: str, api_key: str) -> Optional[NewsArticle]:
    """Fetch trending news for the given location using a news API."""
    endpoint = "https://newsapi.org/v2/top-headlines"
    params = {"q": location, "apiKey": api_key}
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("articles"):
            first = data["articles"][0]
            return NewsArticle(
                title=first.get("title", ""),
                content=first.get("content", ""),
                url=first.get("url", ""),
            )
    except Exception as exc:
        print(f"Error fetching news: {exc}")
    return None


def rewrite_article_with_openai(article: NewsArticle, location: str, api_key: str) -> str:
    """Use OpenAI to rewrite the article optimized for the given location."""
    openai.api_key = api_key
    prompt = (
        f"Rewrite the following article so it targets readers in {location}. "
        "Keep all important facts, but improve clarity and local SEO.\n\n"
        f"Title: {article.title}\n\n{article.content}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        print(f"OpenAI rewrite error: {exc}")
        return article.content


def generate_podcast_script(article: NewsArticle, location: str) -> str:
    """Generate a short podcast script."""
    return (
        f"Welcome to our {location} news podcast. Today we discuss: {article.title}. "
        f"Here are the details: {article.content}"
    )


def generate_youtube_short_script(article: NewsArticle, location: str) -> str:
    """Generate a short script for a YouTube short video."""
    return (
        f"Hey {location}! Here's a quick update: {article.title}. "
        f"Check out more on our blog!"
    )


def generate_images_with_openai(prompt: str, api_key: str, num_images: int = 2) -> List[str]:
    """Generate images using OpenAI's image API and return local file paths."""
    openai.api_key = api_key
    paths: List[str] = []
    try:
        response = openai.Image.create(prompt=prompt, n=num_images, size="1024x1024")
        for idx, item in enumerate(response.get("data", [])):
            img_url = item.get("url")
            if not img_url:
                continue
            img_resp = requests.get(img_url, timeout=10)
            img_resp.raise_for_status()
            path = f"generated_image_{idx}.png"
            with open(path, "wb") as f:
                f.write(img_resp.content)
            paths.append(path)
    except Exception as exc:
        print(f"OpenAI image generation error: {exc}")
    return paths


def create_qr_code(data: str, path: str) -> str:
    """Create a QR code image containing the given data."""
    qr_img = qrcode.make(data)
    qr_img.save(path)
    return path


def create_youtube_video(image_paths: List[str], qr_path: str, output: str) -> None:
    """Create a simple slideshow video from images with a QR code watermark."""
    clips = [ImageClip(p).set_duration(3) for p in image_paths]
    if not clips:
        return
    base = concatenate_videoclips(clips, method="compose")
    watermark = ImageClip(qr_path).set_duration(base.duration).resize(height=150).set_pos(("right", "bottom")).set_opacity(0.8)
    final = CompositeVideoClip([base, watermark])
    final.write_videofile(output, fps=24)


def post_to_youtube(video_path: str, title: str, description: str) -> None:
    """Placeholder for posting a video to YouTube."""
    print(f"Posting {video_path} to YouTube with title '{title}'")


def post_to_podcast(audio_path: str, feed_url: str) -> None:
    """Placeholder for uploading podcast audio to RSS feed."""
    print(f"Uploading podcast {audio_path} to feed {feed_url}")


def publish_to_wordpress(title: str, body: str, youtube_link: str, podcast_link: str) -> None:
    """Placeholder for publishing content to Wordpress."""
    print(f"Publishing '{title}' to Wordpress with video {youtube_link} and podcast {podcast_link}")


def run_workflow(location: str, news_api_key: str, openai_key: str) -> None:
    article = fetch_local_trending_news(location, news_api_key)
    if not article:
        print("No news article found.")
        return
    rewritten = rewrite_article_with_openai(article, location, openai_key)
    podcast_script = generate_podcast_script(article, location)
    youtube_script = generate_youtube_short_script(article, location)

    images = generate_images_with_openai(f"{article.title} {location}", openai_key, 2)
    qr_code = create_qr_code(article.url or "https://example.com", "qr.png")
    create_youtube_video(images, qr_code, "short.mp4")

    # Placeholder calls
    post_to_youtube("short.mp4", article.title, youtube_script)
    post_to_podcast("audio.mp3", "https://rss.com/myfeed")
    publish_to_wordpress(article.title, rewritten, "https://youtube.com/short", "https://rss.com/myfeed/episode1")

    print("Workflow completed.")


if __name__ == "__main__":
    # Replace with real API keys and location
    run_workflow("New York", "YOUR_NEWS_API_KEY", "YOUR_OPENAI_API_KEY")

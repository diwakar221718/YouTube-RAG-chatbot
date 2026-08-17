# youtube_utils.py

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


# ============================================================
# 1. Extract YouTube Video ID
# ============================================================

def extract_video_id(url):

    try:
        parsed_url = urlparse(url)

        # Normal YouTube URL
        # https://www.youtube.com/watch?v=VIDEO_ID
        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:

            video_id = parse_qs(
                parsed_url.query
            ).get("v", [None])[0]

            return video_id

        # Short YouTube URL
        # https://youtu.be/VIDEO_ID
        elif parsed_url.hostname == "youtu.be":

            return parsed_url.path.lstrip("/")

        # YouTube Shorts
        # https://www.youtube.com/shorts/VIDEO_ID
        elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:

            if parsed_url.path.startswith("/shorts/"):

                return parsed_url.path.split("/")[2]

        return None

    except Exception:
        return None


# ============================================================
# 2. Get YouTube Transcript
# ============================================================

def get_transcript(video_id):

    try:

        if not video_id:
            return None, "Invalid YouTube video ID."

        # Create API object
        api = YouTubeTranscriptApi()

        # Fetch transcript
        transcript_data = api.fetch(video_id)

        # Convert transcript snippets into one string
        transcript = " ".join(
            snippet.text
            for snippet in transcript_data
        )

        if not transcript.strip():
            return None, "Transcript is empty."

        return transcript, None

    except Exception as e:

        return None, f"Could not retrieve transcript: {str(e)}"


# ============================================================
# 3. Get Transcript Directly From YouTube URL
# ============================================================

def get_transcript_from_url(url):

    # Extract video ID
    video_id = extract_video_id(url)

    if not video_id:

        return None, None, "Invalid YouTube URL."

    # Get transcript
    transcript, error = get_transcript(video_id)

    if error:

        return None, video_id, error

    return transcript, video_id, None
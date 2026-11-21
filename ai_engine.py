
import os
import json
import time
from moviepy import VideoFileClip
from google import genai
from google.genai import types
from dotenv import load_dotenv
from database import get_brand

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.8-flash"


def generate_content(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text



def analyze_video(video_path):
    with open(video_path, "rb") as file:
        video_bytes = file.read()

    video_part = types.Part.from_bytes(
        data=video_bytes,
        mime_type="video/mp4"
    )

    brand = get_brand()

    if brand:
        brand_context = f"""
        Brand name: {brand[1]}
        Preferred tone: {brand[2]}
        Preferred hashtags: {brand[3]}
        Caption style: {brand[4]}
        """
    else:
        brand_context = "Use a friendly and engaging tone."

    prompt = f"""
    Analyze this video for a content creator.

    Brand preferences:
    {brand_context}

    Give me:
    1. Short video summary.
    2. Three interesting moments.
    3. Start and end timestamps.
    4. Reasons for selecting each moment.
    5. Instagram captions.
    6. YouTube titles.
    7. LinkedIn captions.

    Follow the brand preferences when writing all captions and titles.
    Use the saved hashtags in the captions.

    Return the result in a clear structured format.
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=[video_part, prompt]
    )

    return response.text



def find_highlights(video_path):
    with open(video_path, "rb") as file:
        video_bytes = file.read()

    video_part = types.Part.from_bytes(
        data=video_bytes,
        mime_type="video/mp4"
    )

    prompt = """
    Analyze this video and find the 3 most interesting moments.

    Return ONLY valid JSON in this format:

    {
        "highlights": [
            {
                "title": "Highlight title",
                "start": 5,
                "end": 20,
                "reason": "Why this moment is interesting"
            }
        ]
    }

    Start and end must be timestamps in seconds.
    End must be greater than start.
    Select moments that exist in the video.
    Do not include markdown outside JSON.
    """

    print("ACTIVE GEMINI MODEL:", MODEL)

    response = client.models.generate_content(
        model=MODEL,
        contents=[video_part, prompt]
    )

    return response.text


   
   
           

    


def create_clip(video_path, start_time, end_time, output_path):
    video = VideoFileClip(video_path)

    clip = video.subclipped(start_time, end_time)

    clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    clip.close()
    video.close()

    return output_path


if __name__ == "__main__":
    result = generate_content(
        "Give me 3 catchy captions for a motivational video."
    )
    print(result)
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import json


# Replace with your API key
load_dotenv()
API_KEY = os.getenv('YOUTUBE_KEY')
CHANNEL_ID = "UCNcWiCgpHVctNxLr3FD04PA"  # Example: Hololive Official
handle = "@Sentinels"

# Create a YouTube service client
youtube = build("youtube", "v3", developerKey=API_KEY)

with open("channels.json") as f:
    data = json.load(f)

for member in data["channels"]:
    theid = member["id"]
    name = member["name"]


    request = youtube.search().list(
        part="snippet",
        channelId=theid,
        eventType="live",
        type="video"
    )

    response = request.execute()

    if response["items"]:
        video = response["items"][0]
        title = video["snippet"]["title"]
        video_id = video["id"]["videoId"]
        print(f"{name} is LIVE now!")
        print(f"https://www.youtube.com/watch?v={video_id}")
    else:
        print(f"⚫{name} is not currently live.")







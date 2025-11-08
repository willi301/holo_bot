import discord
from discord.ext import commands
import os
import logging
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
import json
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

#######youtube api stuff#######
# Replace with your API key
API_KEY = os.getenv('YOUTUBE_KEY')


def get_live_channels(api_key: str, json_path: str):
    """Return a list of currently live channels."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    youtube = build("youtube", "v3", developerKey=api_key)
    live_channels = []

    for member in data["channels"]:
        channel_id = member["id"]
        name = member["name"]

        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            eventType="live",
            type="video"
        )

        response = request.execute()

        if response.get("items"):
            video = response["items"][0]
            live_channels.append({
                "name": name,
                "title": video["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={video['id']['videoId']}"
            })

    return live_channels

# Create a YouTube service client




handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready to go!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please watch your language!")

    # keeps checking for commands after on_message event
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def who(ctx):
    await ctx.send(f'I am holobot, your friendly Discord bot!')

@bot.command()
async def live(ctx):
    await ctx.send("⏳ Checking who’s live... please wait...")

    try:
        channel_list = await asyncio.to_thread(get_live_channels, API_KEY, "channels.json")
    except Exception as e:
        await ctx.send(f"❌ Error while getting channels: {e}")
        raise  # also prints full traceback in console

    if channel_list:
        live_msg = "🔴 These channels are currently live:\n"
        for channel in channel_list:
            live_msg += f"• **{channel['name']}** → <{channel['url']}>\n"
        await ctx.send(live_msg)
    else:
        await ctx.send("⚫ No channels are currently live right now.")




bot.run(token, log_handler=handler, log_level=logging.DEBUG)








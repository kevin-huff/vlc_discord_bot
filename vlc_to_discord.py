import os
import sys
import requests
import math
from xml.etree import ElementTree
import discord
from dotenv import load_dotenv
from discord.ext import tasks
import vlc

# Load Discord bot token and channel ID from the environment
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))
VLC_HTTP_PASSWORD = os.getenv("VLC_HTTP_PASSWORD")
ALWAYS_SKIP_USERS = [int(user_id.strip()) for user_id in os.getenv("ALWAYS_SKIP_USERS").split(',')]

# Set intents for the Discord bot
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

async def send_message(channel, message):
    await channel.send(message)

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    channel = client.get_channel(CHANNEL_ID)
    track_info.start(channel)
    
    # Connect to the voice channel
    guild = channel.guild
    voice_channel = guild.get_channel(VOICE_CHANNEL_ID)
    await voice_channel.connect()

skip_votes = {}

@client.event
async def on_message(message):
    global skip_votes
    if message.content.lower() == "!skip" and message.channel.id == CHANNEL_ID:
        user_id = message.author.id
        skip_votes[user_id] = True

        # Check if the video should be skipped
        voice_channel = message.guild.get_channel(VOICE_CHANNEL_ID)
        if should_skip_video(voice_channel.members):
            await skip_video()
            skip_votes = {}

def should_skip_video(members):
    total_users = len([member for member in members if not member.bot])
    vote_count = len(skip_votes)
    print(f"{vote_count} / {total_users} users have voted to skip.")
    # Check if any of the special users have voted to skip
    special_user_vote = any(user_id in ALWAYS_SKIP_USERS for user_id in skip_votes)

    # More than 2/3rds of the users have voted to skip, or a special user has voted
    return vote_count >= math.ceil(total_users * 2 / 3) or special_user_vote


async def skip_video():
    try:
        requests.post("http://localhost:8080/requests/playlist.xml?command=pl_next", auth=("", VLC_HTTP_PASSWORD))
        print("Video skipped.")
    except requests.exceptions.RequestException:
        print("Error skipping video.")

def get_vlc_media_info():
    try:
        response = requests.get("http://localhost:8080/requests/status.xml", auth=("", VLC_HTTP_PASSWORD))
        response.raise_for_status()
        tree = ElementTree.fromstring(response.content)
        filename_element = tree.find(".//category[@name='meta']/info[@name='filename']")
        if filename_element is not None:
            return filename_element.text
        else:
            return None
    except requests.exceptions.RequestException:
        return None

last_video_title = None

@tasks.loop(seconds=5)
async def track_info(channel):
    global last_video_title
    video_title = get_vlc_media_info()

    if video_title and video_title != last_video_title:
        truncated_title = video_title[:10]
        await send_message(channel, f"Currently playing: {truncated_title}")
        last_video_title = video_title
    elif video_title is None:
        last_video_title = None
    else:
        print("No new video is currently playing.")

# Run the Discord bot
client.run(TOKEN)

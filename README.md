# VLC to Discord Notifier and Vote-to-Skip Bot

This script allows you to send notifications to a specific Discord channel when a new video starts playing in VLC Media Player. Additionally, it includes a vote-to-skip feature that lets users in a voice channel vote to skip the currently playing video.

## Requirements

- Python 3.7 or higher
- VLC Media Player with the HTTP Interface enabled
- A Discord bot with the `messages` and `message_content` intents enabled

## Dependencies

Install the required Python libraries using the following command:

```
pip install discord.py python-dotenv requests python-vlc
```

## Setup

1. Enable the HTTP interface in VLC Media Player:
   - Go to Tools -> Preferences
   - Change "Show settings" to "All"
   - Navigate to Interface -> Main interfaces
   - Check the "Web" option
   - Navigate to Interface -> Main interfaces -> Lua
   - Set a password for the HTTP interface in the "Lua HTTP" section

2. Create a `.env` file in the same directory as the Python script with the following content:
```
DISCORD_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_discord_channel_id
VOICE_CHANNEL_ID=your_voice_channel_id
VLC_HTTP_PASSWORD=your_vlc_http_password
ALWAYS_SKIP_USERS=user_id1,user_id2
```

Replace the placeholders with your actual Discord bot token, channel ID, voice channel ID, VLC HTTP password, and the user IDs of users with the "always skip" privilege.

## Running the script

Run the script using the following command:

```
python3 vlc_to_discord.py
```

Once the bot is running, it will send a message to the specified Discord channel whenever a new video starts playing in VLC Media Player. Users can vote to skip the video by typing `!skip` in the channel.

## Vote-to-skip rules

To skip a video, more than 2/3rds of the users in the voice channel need to vote. Users with the "always skip" privilege can skip a video with just their vote.

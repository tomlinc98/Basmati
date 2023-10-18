import discord
import json
import os
import yt_dlp
from discord.ext import commands

# Load the token from config.json
with open('config.json', 'r') as file:
    config = json.load(file)
    token = config.get('token')

intents = discord.Intents.all()  # Declare the intents you're using
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.event
async def on_message(message):
    if 'https://x.com/' in message.content:
        await message.delete()
        new_url = message.content.replace('https://x.com/', 'https://fxtwitter.com/')
        await message.channel.send(new_url)
    elif 'https://www.tiktok.com/' in message.content:
        url = message.content

        # Ensure the 'downloads' directory exists
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        # Options for yt-dlp
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]',  # Get the best quality video format
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save the video in a folder named 'downloads'
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferredformat': 'mp4',
            }],
            'quiet': False
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Using yt-dlp directly
                info_dict = ydl.extract_info(url, download=True)
                video_file = ydl.prepare_filename(info_dict)

            # Upload the video to Discord
            with open(video_file, 'rb') as fp:
                await message.channel.send(file=discord.File(fp, 'video.mp4'))

            # Delete the video file from the server
            os.remove(video_file)
        except Exception as e:
            await message.channel.send(f"Error processing the video: {e}")

    await bot.process_commands(message)

# Run the bot
bot.run(token)

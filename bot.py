import os
import yt_dlp
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import Activity, ActivityType, Status

# Load the token from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()  # Declare the intents you're using
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Set the bot's status to display the current date and time
    await bot.change_presence(activity=Activity(type=ActivityType.watching, name=f"you"), status=Status.online)
    print(f'{bot.user.name} is ready!')

@bot.event
async def on_message(message):
    if 'https://x.com/' in message.content or 'https://twitter.com/' in message.content:
        # Check if the message has any embeds
        if message.embeds:
            return  # The link is already embedded, so we don't need to do anything

        new_url = message.content.replace('https://x.com/', 'https://fxtwitter.com/').replace('https://twitter.com/', 'https://fxtwitter.com/')
        await message.reply(f"Here's the fixed embed: {new_url}")  # Reply to the user with the modified link
    elif 'https://vm.tiktok.com/' in message.content:
        url = message.content

        # Ensure the 'downloads' directory exists
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        # Options for yt-dlp
        ydl_opts = {
            'format': 'best',  # Automatically select the best available format
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save the video in a folder named 'downloads'
            'quiet': False
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Using yt-dlp directly
                info_dict = ydl.extract_info(url, download=True)
                video_file = ydl.prepare_filename(info_dict)

            # Upload the video to Discord
            with open(video_file, 'rb') as fp:
                await message.channel.send(f"{message.author.mention}, here's the video:", file=discord.File(fp, 'video.mp4'))

            # Delete the video file from the server
            os.remove(video_file)
        except Exception as e:
            await message.channel.send(f"{message.author.mention}, error processing the video: {e}")

    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
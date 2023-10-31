import discord
from discord.ext import commands
import yt_dlp
import os
import aiofiles
import io
import re

class TikTok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.download_path = 'downloads'
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Find all TikTok links in the message
        tiktok_links = re.findall(r'(https://vm.tiktok.com/[^\s]+|https://www.tiktok.com/@\w+/video/\d+)', message.content)

        # Process each TikTok link
        for link in tiktok_links:
            await self.process_tiktok_link(message.channel, link)

    async def process_tiktok_link(self, channel, link):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=True)
                video_file = ydl.prepare_filename(info_dict)
                
                # Check if the downloaded file is an mp3
                if video_file.endswith(".mp3"):
                    await channel.send("This TikTok link is an audio slideshow, and it cannot be processed.")
                    return
                
                # If it's not an mp3, send the video
                async with aiofiles.open(video_file, 'rb') as f:
                    video_content = await f.read()

                await channel.send(file=discord.File(io.BytesIO(video_content), 'video.mp4'))
                os.remove(video_file)
                
        except Exception as e:
            await channel.send(f"Error processing the TikTok video: {e}")

def setup(bot):
    bot.add_cog(TikTok(bot))

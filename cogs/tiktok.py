import discord
from discord.ext import commands
import yt_dlp
import os
import aiofiles
import re
import io
import asyncio
import requests
import aiohttp
import time


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

        tiktok_links = re.findall(r'(https://vm.tiktok.com/[^\s]+|https://www.tiktok.com/@[\w\.]+/video/\d+)', message.content)
        
        print("Found TikTok links:", tiktok_links)  # Debug print statement

        for link in tiktok_links:
            await self.process_tiktok_link(message.channel, link)
            
    async def convert_video(self, input_path, output_path):
        command = [
            'ffmpeg', '-i', input_path, '-c:v', 'libx264', '-crf', '23',
            '-preset', 'fast', '-c:a', 'aac', '-b:a', '192k', '-y', output_path
        ]
        process = await asyncio.create_subprocess_exec(*command)
        await process.communicate()

        if process.returncode != 0:
            raise Exception('FFmpeg conversion failed')

    async def process_tiktok_link(self, channel, link):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
            'outtmpl': f'{self.download_path}/video_{int(time.time())}.%(ext)s',  # Append a timestamp to the filename
        }
        
        processing_message = await channel.send("Processing TikTok video...")

        try:
            clean_link = await self._clean_url(link)  # Clean the URL
        except Exception as e:
            await channel.send(f"Error cleaning the TikTok URL: {e}")
            return

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(clean_link, download=True)  # Use the cleaned URL
                video_file = ydl.prepare_filename(info_dict)
                
                if video_file.endswith(".mp3"):
                    await channel.send("This TikTok link is an audio slideshow, and it cannot be processed.")
                    return
                
                file_size = os.path.getsize(video_file)
                if file_size > 8 * 1024 * 1024:  # 8 MB
                    await channel.send("The video is too large to be uploaded to Discord.")
                    return
                
                converted_file = video_file + ".mp4"
                await self.convert_video(video_file, converted_file)
                
                async with aiofiles.open(converted_file, 'rb') as f:
                    content = await f.read()
                    await channel.send(file=discord.File(io.BytesIO(content), filename='video.mp4'))
                    
                os.remove(video_file)
                os.remove(converted_file)
                
        except yt_dlp.utils.DownloadError as e:
            await channel.send(f"Error downloading the TikTok video: {e}")
        except discord.errors.HTTPException as e:
            await channel.send(f"Error uploading the video to Discord: {e}")
        except Exception as e:
            await channel.send(f"An unexpected error occurred: {e}")
        finally:
            if os.path.exists(video_file):
                os.remove(video_file)
            if os.path.exists(converted_file):
                os.remove(converted_file)

        await processing_message.delete()
                
    async def _clean_url(self, url: str) -> str:
        clean_url = url
        if url.startswith('https://vm.') or url.startswith('https://www.tiktok.com/t/'):
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/39.0.2171.95 Safari/537.36'
                }) as response:
                    response.raise_for_status()
                    return str(response.url)
        return clean_url

def setup(bot):
    bot.add_cog(TikTok(bot))
    
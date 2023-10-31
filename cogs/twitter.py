import discord
from discord.ext import commands
import re

class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Find all Twitter and x.com links in the message
        twitter_links = re.findall(r'(https?://(twitter\.com|x\.com)/[^\s]+)', message.content)

        # Convert each Twitter link to an fxtwitter link and send it
        for link, domain in twitter_links:
            if domain == "x.com":
                new_link = link.replace('https://x.com/', 'https://fxtwitter.com/')
            elif domain == "twitter.com":
                new_link = link.replace('https://twitter.com/', 'https://fxtwitter.com/')
            await message.channel.send(new_link)

def setup(bot):
    bot.add_cog(Twitter(bot))

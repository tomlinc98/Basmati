from discord_slash import cog_ext, SlashContext
from discord.ext import commands
import discord

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="about")
    async def _about(self, ctx: SlashContext):
        embed = discord.Embed(title="About Basmati", description="Basmati is a Discord.py bot with niche utilities designed to enhance your Discord experience. It was created to make communication and content sharing among friends more convenient.", color=0x00ff00)
        embed.add_field(name="GitHub Repository", value="https://github.com/tomlinc98/Basmati", inline=False)
        
        # Current features
        embed.add_field(name="Embeds Twitter / x.com Links", value="Basmati can embed links from x.com (formerly Twitter) using the power of fxtwitter, making it easier to share and discuss tweets within your Discord server.", inline=False)
        embed.add_field(name="TikTok Video Downloads", value="Basmati simplifies the process of sharing TikTok videos with your friends. Simply paste a TikTok video link into the chat, and Basmati will download and upload the video, allowing for easy viewing directly within Discord.", inline=False)
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(About(bot))
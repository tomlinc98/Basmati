import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="💀"), status=discord.Status.online)
    print(f'{bot.user.name} is ready!')

extensions = ['cogs.twitter', 'cogs.tiktok', 'cogs.about']

for extension in extensions:
    try:
        bot.load_extension(extension)
        print(f'Successfully loaded extension: {extension}')
    except Exception as e:
        print(f'Failed to load extension {extension}: {e}')

bot.run(TOKEN)

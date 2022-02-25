import discord
from discord.ext import commands
from discord.utils import get
import nacl
import youtube_dl
from music_cog import music_cog
from main_cog import main_cog

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
bot = commands.Bot(command_prefix = "==", intents = intents)

bot.add_cog(music_cog(bot))
bot.add_cog(main_cog(bot))


with open('token.txt') as data:
    bot.run(data.readline())
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
#.f music

# @bot.command()
# async def join(ctx):
#     voice_channel = ctx.author.voice.channel
#     voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
#     if not voice.is_connected():
#         try:
#             await voice_channel.connect()
#         except:
#             print("Couldn't find the channel")
#     else:
#         print("The bot is already connected to a channel")

# @bot.command()
# async def leave(ctx):
#     voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
#     if voice.is_connected():
#         try:
#             await voice.disconnect()
#         except:
#             print("Couldn't find the channel")
#     else:
#         print("The bot is not connected to a channel")

# @bot.command()
# async def play(ctx):
#     voice_channel = ctx.author.voice.channel
#     voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
#     if not voice.is_connected():
#         try:
#             await voice_channel.connect()
#         except:
#             print("Couldn't find the channel")
#     else:
#         print("The bot is already connected to a channel")

# @bot.command()
# async def pause(ctx):
#     voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
#     if voice.is_playing():
#         voice.pause()
#     else:
#         print("The bot is not playing")

# @bot.command()
# async def resume(ctx):
#     voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
#     if voice.is_paused():
#         voice.resume()
#     else:
#         print("The bot is already playing")

# @bot.command()
# async def stop(ctx):
#     voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
#     voice.stop()

    

with open('token.txt') as data:
    bot.run(data.readline())
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from discord.utils import get
bot = commands.Bot(command_prefix = '==')

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.queue = []
        self.vc = None
        self.current_channel = None

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 - reconnect_delay_max 5', 'options': '-vn'}
    
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                song = ydl.extract_info('ytsearch:%s' % item, download = False)['entries'][0]
                url = song['formats'][0]['url']
                title = song['title']
            except Exception:
                return False

        return {'url': url, 'title': title}

    async def start_play(self, ctx):
        if len(self.queue) > 0:
            current_url = self.queue[0]['url']
            current_title = self.queue[0]['title']
            self.queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(current_url, **self.FFMPEG_OPTIONS), after = lambda e: self.next())
            print('start playing')
            await ctx.send(f'{current_title}')

    def next(self):
        if len(self.queue) > 0:
            current_url = self.queue[0]['url']
            current_title = self.queue[0]['title']
            self.queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(current_url, **self.FFMPEG_OPTIONS), after = lambda e: self.next())




    @commands.command()
    async def search(self, ctx, *args):
        item = ' '.join(args)
        info = self.search_yt(item)
        print(info)

    @commands.command()
    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel
        try:
            #   self.vc = await ctx.guild.change_voice_state(channel = voice_channel)
            self.vc = await voice_channel.connect()
            self.current_channel = voice_channel
        except AttributeError:
            await ctx.send("Join a voice channel", delete_after = 5)
        print('is_connected' , self.vc.is_connected())
        #except discord.errors.ClientException:
            #await ctx.send("Mewsic is already connected to a channel", delete_after = 5)
        #self.voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)

    @commands.command()
    async def play(self, ctx, *args):
        searching_for = ' '.join(args)

        voice_channel = ctx.author.voice.channel
        if self.current_channel == None or voice_channel is not self.current_channel:
            try:
                self.vc = await voice_channel.connect()
                self.current_channel = voice_channel
            except AttributeError:
                await ctx.send("Join a voice channel", delete_after = 5)
                return 0
            except discord.errors.ClientException:
                await ctx.send("Mewsic is already connected to another channel", delete_after = 5)
                return 0
        
        song = self.search_yt(searching_for)
        self.queue.append(song)

        if self.vc.is_playing() == False:
            await self.start_play(ctx)
        


    @commands.command()
    async def leave(self, ctx):
        try:
            await self.vc.disconnect()
            self.vc = None
            self.current_channel = None
        except AttributeError:
            await ctx.send("Mewsic is not connected to a channel", delete_after = 5)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print('state update')
        if member.bot and before.channel != None and after.channel == None:
            self.vc.cleanup()
            # self.current_channel = None
            # self.queue = []
            # print(self.vc)
            #print('is_connected', self.vc.is_connected())

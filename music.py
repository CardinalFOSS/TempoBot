import discord
from discord.ext import commands
import youtube_dl
import math

SongList = []

class music(commands.Cog):
  def _init_(self, client):
        self.client = client
    
  @commands.command()
  async def join(self, ctx):
      if ctx.author.voice is None:
          await ctx.send(":x: **You have to be in a voice channel to use this command!**")
      voice_channel = ctx.author.voice.channel
      if ctx.voice_client is None:
          await voice_channel.connect()

          VCName = str(voice_channel)
          VCMention = voice_channel.mention
          await ctx.send(":thumbsup: **Joined** " + "`" + VCName + "`" + "** and bound to** " + VCMention )
      else:
          await ctx.voice_client.moveto(voice_channel)

  @commands.command()
  async def leave(self, ctx):
      await ctx.voice_client.disconnect()

  @commands.command()
  async def p(self, ctx, url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format':"bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          url2 = info['formats'][0]['url']
          source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
          vc.play(source)
        
        info_dict = ydl.extract_info(url, download=False)
        video_url = info_dict.get("url", None)
        video_title = info_dict.get('title', None)
        video_author = info_dict.get('creator', None)
        video_thumbnail = info_dict.get('thumbnail', None)
        video_duration = info_dict.get('duration', None)

        Minutes = math.floor(video_duration/60)
        Seconds = video_duration%60
        ConvertDuration = str(Minutes) + ":" + str(Seconds)

        SongEmbed = discord.Embed(title=video_title, url=video_url,  color=2303786)

        SongEmbed.set_author(name="Added To Queue", icon_url="https://bit.ly/3xpOFPc")
        SongEmbed.set_thumbnail(url=video_thumbnail)


        SongEmbed.add_field(name="Channel", value=video_author, inline=True)
        SongEmbed.add_field(name="Song Duration", value=ConvertDuration, inline=True)
        SongEmbed.add_field(name="\u200b", value="\u200b", inline=True)

        SongEmbed.add_field(name="Estimated time until playing", value="2:30",inline=True)
        SongEmbed.add_field(name="Position in queue", value="1", inline=True)
        SongEmbed.add_field(name="\u200b", value="\u200b", inline=True)
      
        SongList.append(video_title)
        await ctx.send(embed=SongEmbed)

  @commands.command()
  async def pause(self, ctx):
      await ctx.send("Player Paused")
      ctx.voice_client.pause()
       
  @commands.command()
  async def resume(self, ctx):
      await ctx.send("Player Resumed")
      ctx.voice_client.resume()

  @commands.command()
  async def q(self, ctx):
    QueueEmbed = discord.Embed(title="Queue for " + str(ctx.guild.name), url="https://bit.ly/3xpOFPc", color=discord.Color.lighter_grey())

    for v in SongList:
      QueueEmbed.add_field(name="93", value=v, inline=False)

    print(SongList)

    await ctx.send(embed=QueueEmbed)

def setup(client):
    client.add_cog(music(client))
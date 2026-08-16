import discord
from discord.ext import commands
import random
import os
import yt_dlp

class Communicate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    cog_folder = os.path.dirname(__file__)
    dirname = os.path.split(cog_folder)[0]
    voicelines = os.path.join(dirname, "textfiles/voicelines.txt")
    lyrics = os.path.join(dirname, "textfiles/lyrics.txt")
    faq_file = os.path.join(dirname, "textfiles/faq.txt")
    music_playlist = "https://youtube.com/playlist?list=PLo5TutRtnZA5v-NVYH5q0aJLr0d420vOg"
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(music_playlist, download=False, process=False)
        list_of_songs = [f"{x['title']}<>{x['uploader']}" for x in info['entries']]
        


    @discord.slash_command(name="hello", description="Say hi to our beloved PINAS:3")
    async def hello(self, ctx):
        await ctx.response.send_message(random.choice(open(self.voicelines).readlines()))

    @discord.slash_command(name="speak", description="See if PINAS can offer any words of wisdom")
    async def speak(self, ctx):
        await ctx.response.send_message(random.choice(open(self.lyrics).readlines()))

    @discord.slash_command(name="faq", description="inFrequently Asked Questions")
    async def faq(self, ctx):
        a = open(self.faq_file).read()
        await ctx.response.send_message(a, ephemeral = True)

    @discord.slash_command(name="reccomend", description="Ask PINAS for a music reccomendation")
    async def reccomend(self, ctx):
        random_song = random.choice(self.list_of_songs)
        song_string = f"{random_song.split('<>')[0]} by {random_song.split('<>')[1]}"
        await ctx.response.send_message(song_string, ephemeral = True)


def setup(bot):
    bot.add_cog(Communicate(bot))
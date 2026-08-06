import discord
from discord.ext import commands
import random
import os

class Communicate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    cog_folder = os.path.dirname(__file__)
    dirname = os.path.split(cog_folder)[0]
    voicelines = os.path.join(dirname, "textfiles/voicelines.txt")
    lyrics = os.path.join(dirname, "textfiles/lyrics.txt")
    faq_file = os.path.join(dirname, "textfiles/faq.txt")

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


def setup(bot):
    bot.add_cog(Communicate(bot))
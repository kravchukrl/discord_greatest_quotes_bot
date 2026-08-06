import discord
from discord.ext import commands
import json
import os
import sys
cog_folder = os.path.dirname(__file__)
dirname = os.path.split(cog_folder)[0]
configs = os.path.join(dirname, "utils/")
sys.path.append( configs )
from utils.server_vars import server_to_quotes, server_to_threshold, server_to_restricted

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    cog_folder = os.path.dirname(__file__)
    dirname = os.path.split(cog_folder)[0]
    about_file = os.path.join(dirname, "textfiles/about.txt")
    about_text = open(about_file).read()

    @discord.slash_command(name="about", description="explaining PINAS functionality and commands")
    async def about(self, ctx):
        qt_chan = self.bot.get_channel(server_to_quotes[ctx.guild_id])
        # Quotes channel name/link qt_chan = self.bot.get_channel(server_to_quotes[ctx.guild_id])
        # Server Name - ctx.guild
        # Threshold - server_to_threshold[ctx.guild_id] 
        about_fixed = self.about_text.replace('{quotes}', f'**#{qt_chan.name}**').replace('{server}', f'**{ctx.guild.name}**').replace('{number}', f'**{server_to_threshold[ctx.guild_id]}**')
        await ctx.response.send_message(about_fixed, ephemeral=True)

    
        
        
def setup(bot):
    bot.add_cog(About(bot))
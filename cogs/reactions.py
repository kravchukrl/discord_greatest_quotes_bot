import discord
from discord.ext import commands
import json
import os
import sys
cog_folder = os.path.dirname(__file__)
dirname = os.path.split(cog_folder)[0]
configs = os.path.join(dirname, "utils/")
sys.path.append( configs )
from utils.server_vars import server_to_quotes, server_to_threshold

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    user_message_cache = {}

    PIN_EMOJI = "📌"
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        current_server = reaction.message.guild.id
        current_quote = server_to_quotes[current_server]
        channel = self.bot.get_channel(current_quote)
        current_threshold = server_to_threshold[current_server]
        react_emoji = reaction.emoji
        react_count = reaction.count
        current_message_id = reaction.message.id
        if not(current_message_id in self.user_message_cache): self.user_message_cache[current_message_id] = []
        unique_list = self.user_message_cache[current_message_id]
        if react_emoji == self.PIN_EMOJI and not(user.id in unique_list):
            # adding users that have reacted to a list, to avoid duplication when re-reaching threshold
            if react_count == 1:
                unique_list.append(user.id)
            else: 
                unique_list.append(user.id)
            # basic reaction functionality, condition for resending attachments
            if len(unique_list) == current_threshold:
                if not reaction.message.attachments: await channel.send("\"" + reaction.message.content + "\" - " + reaction.message.author.name)
                else: 
                    await channel.send(reaction.message.attachments[0].url)
                    await channel.send(f"Courtesy of {reaction.message.author.name}")
        
        
def setup(bot):
    bot.add_cog(Reactions(bot))
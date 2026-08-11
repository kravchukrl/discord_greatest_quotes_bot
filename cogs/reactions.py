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

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # following cache stores message.id as key and a list, populated by user.id, as values
    user_message_cache = {}

    PIN_EMOJI = "📌"
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # establishing which server we're in, what's the channel for quotes, the threshold etc.
        current_server = reaction.message.guild.id
        current_quote = server_to_quotes[current_server]
        channel = self.bot.get_channel(current_quote)
        current_threshold = server_to_threshold[current_server]
        react_emoji = reaction.emoji
        react_count = reaction.count
        current_message_id = reaction.message.id
        # creating empty list ahead of a chaeck
        if not(current_message_id in self.user_message_cache): self.user_message_cache[current_message_id] = []
        unique_list = self.user_message_cache[current_message_id]
        if react_emoji == self.PIN_EMOJI and not(user.id in unique_list):
            # adding users that have reacted to a list, to avoid duplication when re-reaching threshold
            unique_list.append(user.id)

            # if react_count == 1:
            #     unique_list.append(user.id)
            # else: 
            #     unique_list.append(user.id)

            # restricted channels functionality
            if reaction.message.channel.id in server_to_restricted[current_server]:
                replying = await reaction.message.reply("Could not pin the message. The channel is ŗ̶̡̨̛̤̤̪̥̼̻̗̯̺̟̞͍͇͎͖̭̳̭̐̌̅̉̈́̓́̓̅̌̍͒̅̌̃̂̑̎͒͌̾́͊̒̋͋̕͜ę̷̢̪̩͚̗̖̮̙̭̙̤̩̝̖̼͎͉͎̼͖̱̹̭͙̩̤̳̤̝̥̩̯̖̗̬͎̒̇̈́͑͆̀̊̃́͆́͛̐̂́̇̈̾͗͋̒̈́̿͐̽͆̋̓̋̌̎͒͗̎͋̑̓͋̓̎͂̕̚͜͝͠ͅs̴̡̨̛̖̙̼̜͕̬̜͈̦͕̥̹̦̺͕̜̺̼̫̻̬͖͍͉̪͔̝̻̲̲̗̪̬̜̼̺̯͖̫͐̀̊͛̆̉̉̎͒̆͊̎̃͆̔͐̾̈̄͐͆́͐̐̔̇̾̄̀͘͘͝͝͠t̸̢̧̼̗͉̖͈̖̞͇̬̖̩̥̠̗̦̠̹̙̘͋̓̇͛͒͑̋̈́̊̾̒͜͜ŗ̵̳̻̲̾̄͑̽̌̐͋̒̂̌̅̉͋̆̄͆͛́̓͗̎́̋́̽͒͛̆́͐̑̌̏̑̍̿̌͆͒̍̏̌͘̚͘͝͝͝͝ị̵̅̃̆̀̈̔́̉̏̃́̊͂̋̎̏͐̂̈́͐̐͆̓̔͑͑̏̅̐͌̂̂͆͛̋̐̿̚̚͘̚͠͝͝͠͠c̴̢̧̢̞͚̲͔͈̰̭̯͈̤̲̰͎̦̻͔͖͙̖̣͎̈́̎̅̓̇̽̌̐̔̾̏̓̾̒͑̄̿̀̈́̑͆̋̍̓̓̾̿̃̄̅̈́̔̋͋͊̃̕̚̕͘̕͘͠ͅt̴̡̧̨̛͈̖͔̞̫̭̟͈̝̹̤̳̼̱̮̠̹̼̞̖̯̹͕̩͙̩̱͚̏͗̽͛͗͂̓̒̾̽͛̑̓͆̅̀́̌̽͆̿̐͌̾͑̾̏̅̑̅̃̾̌̇̓͌̕̚̚̚̕͜͜͜͠͝͝͝ͅę̶̢̫̪͚͉̜̯̟̘̹͈̦̟̻̮̲̮̣͔̲̖͍̗̳̜͇̗͖͚̹̤̭̜͕͕̼͒̀̃͐̃̿̇͊́̃̀̽͆̊̐͆͛̔͊̔̀͒̀͒̒̊̾͐̉̈͆̅̓̏̑́̀̕͘̕͘͝͠͝ͅd̴̡̢̛̛̛̛̩̞̼̭͍̮̹̰͓̩̞̤̯̫͎̠̭̟̰̗̔̉̄̽̓͗̾͆̏̒̈́͆́̏̏͂̉̀̓̂̾͛̈̔͘͜͜͝͝")
                return 
            # basic reaction functionality, condition for resending attachments
            if len(unique_list) == current_threshold:
                if not reaction.message.attachments: await channel.send("\"" + reaction.message.content + "\" - " + reaction.message.author.name)
                else: 
                    await channel.send(reaction.message.attachments[0])
                    await channel.send(f"Courtesy of {reaction.message.author.name}")
        
        
def setup(bot):
    bot.add_cog(Reactions(bot))
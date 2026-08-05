import discord
from discord.ext import commands
import os
import re
import json
import sys
cog_folder = os.path.dirname(__file__)
dirname = os.path.split(cog_folder)[0]
configs = os.path.join(dirname, "utils/")
sys.path.append( configs )
from utils.server_vars import server_to_quotes, server_to_threshold

class Suggesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    y = "Yay:D"
    n = "Nope:p"

    @discord.slash_command(name="suggest", description="Suggest the quote to be added to the greatest quotes channel through PIN.AS")
    async def suggest(self, ctx, quote: str, author: str):
        quote = f"\"{quote}\" - {author}"
        suggest_poll = discord.Poll(
            question = f"Should the quote * {quote} * be added to the list of the greatest?",
            answers = [
                discord.PollAnswer(self.y),
                discord.PollAnswer(self.n)
            ],
            duration = 6
        )
        message = await ctx.response.send_message(poll=suggest_poll)
    poll_cache = {}

    @commands.Cog.listener()
    async def on_raw_poll_vote_add(self, payload):
        current_server = payload.guild_id
        current_quote = server_to_quotes[current_server]
        quote_channel = self.bot.get_channel(current_quote)
        current_threshold = server_to_threshold[current_server]
        channel = self.bot.get_channel(payload.channel_id)
        acc_message = await channel.fetch_message(payload.message_id)
        poll_question = acc_message.poll.question.text
        match1 = re.search(r'\bShould the quote \*', poll_question)
        match2 = re.search(r'\* be added to the list of the greatest\?\Z', poll_question)
        if not (match1 and match2): return None
        else:
            if not (self.poll_cache.get(poll_question)):
                self.poll_cache[poll_question] = dict(yes=0, no=0)
            if payload.answer_id == 1:
                self.poll_cache[poll_question]["yes"]+=1
            elif payload.answer_id == 2:
                self.poll_cache[poll_question]["no"]+=1
        yes_ans, no_ans = self.poll_cache[poll_question].values()
        if yes_ans == current_threshold and yes_ans > no_ans:
            cleaned_quote = poll_question.split("*")[1]
            await quote_channel.send(cleaned_quote)
            await acc_message.poll.end()
        if no_ans == current_threshold and no_ans > yes_ans:
            await acc_message.poll.end()

    @commands.Cog.listener()
    async def on_raw_poll_vote_remove(self, payload):
        current_server = payload.guild_id
        current_quote = server_to_quotes[current_server]
        quote_channel = self.bot.get_channel(current_quote)
        current_threshold = server_to_threshold[current_server]
        channel = self.bot.get_channel(payload.channel_id)
        acc_message = await channel.fetch_message(payload.message_id)
        poll_question = acc_message.poll.question.text
        match1 = re.search(r'\bShould the quote \*', poll_question)
        match2 = re.search(r'\* be added to the list of the greatest\?\Z', poll_question)
        if not (match1 and match2): return None
        else:
            if payload.answer_id == 1:
                self.poll_cache[poll_question]["yes"]+=-1
            elif payload.answer_id == 2:
                self.poll_cache[poll_question]["no"]+=-1
        yes_ans, no_ans = self.poll_cache[poll_question].values()
        print("Yes answers :", yes_ans)
        print("No answers :", no_ans)
def setup(bot):
    bot.add_cog(Suggesting(bot))

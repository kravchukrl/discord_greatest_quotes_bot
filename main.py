import discord
import os
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
dirname = os.path.dirname(__file__)


# establishing Intents
intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    avatar_path = os.path.join(dirname, "utils/pearto.jpg")
    default_activity = discord.Activity(
        name = "jorking it",
        type = discord.ActivityType.listening,
        details = "being awesome and shittily coded",
        url="https://youtu.be/mjSLIej2BO8?si=GgZDyuvh35LdjHB6",
        assets = {
            "large_image": avatar_path,
            "small_image": avatar_path
        },
        buttons = [
            {
                "Listen Along": "https://youtu.be/mjSLIej2BO8?si=GgZDyuvh35LdjHB6"
            }
        ]
        
    )
    await bot.change_presence(status=discord.Status.idle, activity=default_activity)
    print("I'm ready to be used")

# @bot.slash_command(name="hello", description="Say hi to our beloved PINAS:3")
# async def hello(ctx: discord.ApplicationContext):
#     await ctx.respond("I'm in great pain")

cogs_list = [
    "communicate",
    "reactions",
    "suggesting"
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


bot.run(token)
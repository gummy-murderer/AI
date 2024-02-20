import discord
from discord.ext import commands
from pathlib import Path
import os, dotenv
import logging

from discord_bot.message_format import message_format

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")

dotenv_file = dotenv.find_dotenv(str(Path("./").absolute().joinpath(".env")))
dotenv.load_dotenv()
TOKEN = os.environ["DISCORD_BOT_TOKEN"]
CHANNEL_ID = '1207979046630068234'

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} running together with FastAPI!")

@bot.command()
async def welcome(ctx: commands.Context, member: discord.Member):
    await ctx.send(f"Welcome to {ctx.guild.name}, {member.mention}!")

@bot.event
async def on_message(message):
    if message.content == "안녕!":
        await message.channel.send("반가워!")

    if message.content == "반가워!":
        await message.channel.send("안녕!")

    if message.content == "Hello":
        await message.channel.send("Hello!")

async def send_message(messages: list, **kwargs):
    channel = bot.get_channel(int(CHANNEL_ID))
    if channel is None:
        logging.error(f"Failed to find channel with ID {CHANNEL_ID}")
        return
    
    for message in messages:
        try:
            message = message_format(message, kwargs)
            # print(message)
            await channel.send(f"```ansi\n{message}\n```")
        except Exception as e:
            logging.error(f"Error sending message: {e}")

async def run():
    try:
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        await bot.logout()

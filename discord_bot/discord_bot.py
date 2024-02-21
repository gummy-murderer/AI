import discord
from discord.ext import commands
from pathlib import Path
import os, dotenv
import logging

from discord_bot.message_format import message_format

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")

CHANNEL_ID = '1207979046630068234'

@bot.event
async def on_ready():
    message = f"Logged in as {bot.user} running together with FastAPI!"
    print(message)
    await send_message([message])

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

async def run(token):
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.logout()
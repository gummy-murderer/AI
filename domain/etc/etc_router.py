from fastapi import APIRouter, HTTPException
import discord
import json
import asyncio

from domain.etc import etc_schema
from discord_bot.discord_bot import run, send_message

router = APIRouter(
    prefix="/api/etc",
)
             
@router.post("/discord_bot")
async def generate_intro(discord_bot_schema: etc_schema.DiscordBot):
    asyncio.create_task(run(discord_bot_schema.BotToken))
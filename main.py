# Discord dependencies
import discord
import logging
from discord.ext import commands
import os
# Import bot token and others
from apikeys import *
import asyncio


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
activity = discord.Game(name="With a tennis ball")
client = commands.Bot(command_prefix='--', intents=discord.Intents.all(), activity=activity)


@client.event
async def on_ready():
    print("Successfully connected")
    print("-----------------")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load()
        await client.start(BOT_TOKEN)

asyncio.run(main())

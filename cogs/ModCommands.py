import discord
from discord.ext import commands


class ModCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("ModCommands.py is ready")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        ctx.channel.purge(limit=amount)


async def setup(client):
    await client.add_cog(ModCommands(client))

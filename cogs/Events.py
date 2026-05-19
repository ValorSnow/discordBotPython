import discord
from discord.ext import commands
from datetime import datetime
import io


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events.py is ready!")

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.author.bot:
            return
        embed = discord.Embed(colour=0xff0000,
                              description=f"**Message sent by {msg.author.mention} deleted in {msg.channel.mention}**")
        embed.add_field(name="Message content", value=msg.content)
        await self.send_embed(embed, msg)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        bulk_delete = ''
        for message in messages:
            if message.author.bot:
                return
            bulk_delete += f'{message.author.display_name}({message.author.id}) sent at {message.created_at.strftime('%Y %b %d %H-%M-%S')} "{message.content}"\n'
        await self.client.get_channel(1179153224075333775).send(file=discord.File(io.BytesIO(bulk_delete.encode()), filename=f'bulk delete {datetime.now().strftime('%Y %b %d %H-%M-%S')}.txt'))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot: 
            return
        embed = discord.Embed(colour=0xffff00,
                              description=f"**Message sent by {after.author.mention} edited in {after.channel.mention}**")
        embed.add_field(name="Old message", value=before.content, inline=True)
        embed.add_field(name="New message", value=after.content, inline=True)
        await self.send_embed(embed, before)

    async def send_embed(self, embed: discord.Embed, msg: discord.Message):
        embed.set_author(icon_url=msg.author.display_avatar.url, name=msg.author.display_name)
        embed.set_thumbnail(url=msg.guild.icon.url)
        embed.set_footer(text="MarlowsTestbot.py by Marlow Wilde")
        message_logs = self.client.get_channel(1179153224075333775)
        await message_logs.send(embed=embed)

async def setup(client):
    await client.add_cog(Events(client))

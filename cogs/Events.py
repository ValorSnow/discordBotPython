import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events.py is ready!")

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        channel = msg.channel
        content = msg.content
        embed = discord.Embed(colour=0xff0000,
                              description=f"**Message sent by {msg.author.mention} deleted in {channel.mention}**")
        embed.set_author(icon_url=msg.author.display_avatar.url, name=msg.author.display_name)
        embed.set_thumbnail(url=msg.guild.icon.url)
        embed.add_field(name="Message content", value=content)
        embed.set_footer(text="MarlowsTestbot.py by Marlow Wilde")
        message_logs = self.client.get_channel(1179153224075333775)
        await message_logs.send(embed=embed)


async def setup(client):
    await client.add_cog(Events(client))

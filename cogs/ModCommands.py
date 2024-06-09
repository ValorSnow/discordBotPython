import discord
from discord import Color
from discord.ext import commands


class ModCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("ModCommands.py is ready")

    @commands.command(alias='purge')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if ctx.author.bot:
            return
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} message(s) successfully purged!')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, msg: str = 'No reason provided.'):
        if ctx.author.bot:
            return
        if member == ctx.author:
            await ctx.channel.send("You can't kick yourself dummy.")
            return
        if member.roles.pop() >= ctx.guild.me.roles.pop():
            await ctx.channel.send("Cannot kick this user. (user has higher role)")
            return
        await member.send(f'You have been **kicked** from `{ctx.guild.name}` for the following reason: `{msg}`')
        await member.kick(reason=msg)
        await self.makeEmbed(0xff0000, ctx.author, member, "kicked", msg)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User = None, *, msg: str = 'No reason provided.'):
        if user is None:
            await ctx.channel.send('Please enter a user.')
        if ctx.author.bot:
            return
        if user == ctx.author:
            await ctx.channel.send("You can't ban yourself dummy.")
            return
        member = ctx.guild.get_member(user.id)
        if member:
            if member.roles.pop() >= ctx.guild.me.roles.pop():
                await ctx.channel.send("Cannot ban this user. (user has higher role)")
                return
            await member.send(f'You have been **banned** from `{ctx.guild.name}` for the following reason: `{msg}`')
        await ctx.guild.ban(user=discord.Object(id=user.id), reason=msg)
        await self.makeEmbed(0xff0000, ctx.author, user, "banned", msg)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def multiban(self, ctx, users: commands.Greedy[discord.User] = None, *, msg='No reason given.'):
        if ctx.author.bot:
            return
        if not users:
            return await ctx.send('At least one member is required')
        for user in users:
            if user == ctx.author:
                await ctx.channel.send("You can't ban yourself dummy.")
                return
            member = ctx.guild.get_member(user.id)
            if member:
                if member.roles.pop() >= ctx.guild.me.roles.pop():
                    await ctx.channel.send("Cannot ban this user. (user has higher role)")
                    return
                print('Yes')
                await member.send(f'You have been **banned** from `{ctx.guild.name}` for the following reason: `{msg}`')
            await ctx.guild.ban(user=discord.Object(id=user.id), reason=msg)
            await self.makeEmbed(0xff0000, ctx.author, user, "banned", msg)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, msg="No reason given."):
        if ctx.author.bot:
            return
        await ctx.guild.unban(user=discord.Object(id=user.id), reason=msg)
        await self.makeEmbed(0xffff00, ctx.author, user, "unbanned", msg)

    async def makeEmbed(self, colour, author, member, ptype, reason):
        embed = discord.Embed(
            color=colour,
            title=f"User {ptype}",
            description=f"User {member.name} ({member.mention}) has been {ptype}")
        embed.add_field(name='action by', value=author.mention)
        embed.add_field(name='reason', value=reason)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text='MarlowsTestbot.py by Marlow Wilde')
        await self.client.get_channel(1179153287002464366).send(embed=embed)


async def setup(client):
    await client.add_cog(ModCommands(client))

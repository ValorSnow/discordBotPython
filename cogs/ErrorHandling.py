from discord.ext import commands


class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("ErrorHandling.py is ready")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f"Invalid user: {ctx.current_argument}")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing argument")


async def setup(client):
    await client.add_cog(ErrorHandling(client))

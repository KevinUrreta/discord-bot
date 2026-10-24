from discord.ext import commands


class Leave(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="leave")
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            ctx.voice_client.disconnect()

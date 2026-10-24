import wavelink
from discord.ext import commands


class Skip(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return
        player: wavelink.Player = ctx.voice_client

        if player.current is None:
            return
        await player.skip(force=True)
        await ctx.send("skipped")

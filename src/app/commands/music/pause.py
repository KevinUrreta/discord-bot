import wavelink
from discord.ext import commands


class Pause(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="pause")
    async def pause(self, ctx):
        if ctx.voice_client is None:
            return
        player: wavelink.Player = ctx.voice_client

        if not player.playing:
            return
        await player.pause(True)
        await ctx.send("Paused.")

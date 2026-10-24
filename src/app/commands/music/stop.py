import wavelink
from discord.ext import commands


class Stop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="stop")
    async def stop(self, ctx):
        if ctx.voice_client is None:
            return
        player: wavelink.Player = ctx.voice_client

        player.queue.clear()
        await player.stop()
        ctx.send("Stopped")

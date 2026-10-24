import wavelink
from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="clear")
    async def clear(self, ctx):
        if ctx.voice_client is None:
            return
        player: wavelink.Player = ctx.voice_client

        if player.queue.is_empty:
            return
        player.queue.clear()

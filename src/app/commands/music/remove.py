import wavelink
from discord.ext import commands


class Remove(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="remove")
    async def remove(self, ctx, position: int):
        if ctx.voice_client is None:
            return
        player: wavelink.Player = ctx.voice_client
        if player.queue.is_empty:
            return

        playlist= list[wavelink.Playable](player.queue)
        if position < 1 or position > len(playlist):
            return
        player.queue.remove(playlist[position-1])
        ctx.send("Removed {}".format(playlist[position-1]))

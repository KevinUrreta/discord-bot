import wavelink
from discord.ext import commands


class Shuffle(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="shuffle")
    async def shuffle(self, ctx):
        if ctx.voice_client is None:
            return
        player: wavelink.Player = ctx.voice_client
        if player.queue.count < 2:
            return
        player.queue.shuffle()
        ctx.send("Shuffled!")

import wavelink
from discord.ext import commands




class Loop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="loop")
    async def loop(self, ctx):
        if ctx.voice_client is None:
            return
        player: wavelink.Player = ctx.voice_client

        if not player.current:
            return
        player.queue.mode = (
            wavelink.QueueMode.loop
            if player.queue.mode != wavelink.QueueMode.loop
            else wavelink.QueueMode.normal
        )

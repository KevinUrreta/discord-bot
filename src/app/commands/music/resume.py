import wavelink
from discord.ext import commands


class Resume(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="resume")
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return
        player: wavelink.Player = ctx.voice_client
        if not player.paused:
            return
        await player.pause(False)
        ctx.send("Resume successful")
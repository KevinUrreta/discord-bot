import wavelink
from discord.ext import commands

from src.helpers.metadata import get_original_info


class NowPlaying(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="now_playing")
    async def now_playing(self, ctx):
        if ctx.voice_client is None:
            return
        player: wavelink.Player = ctx.voice_client
        track = player.current
        if track is None:
            return
        info = await get_original_info(str(track.uri), track)
        ctx.send("Now Playing: {}".format(info))

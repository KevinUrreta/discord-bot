import asyncio

import wavelink
from discord.ext import commands

from src.helpers.metadata import get_original_info


class Queue(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="queue")
    async def queue(self, ctx):
        if ctx.voice_client is None:
            return
        player: wavelink.Player = ctx.voice_client

        if player.queue.is_empty:
            return

        tracks = list(player.queue)
        info = await asyncio.gather(*(
            asyncio.to_thread(get_original_info, str(track.uri))
            for track in tracks
        ))

        titles = [info["title"] for _ in info]
        message = "\n".join(
            f"{index}. {title}"
            for index, title in enumerate(titles, start=1)
        )
        ctx.send("Now Playing: {}".format(message))

import asyncio

import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed
from src.helpers.metadata import get_original_info


class Queue(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="queue", aliases=["q"])
    async def queue(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.queue.not_connected",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        player: wavelink.Player = ctx.voice_client

        if player.queue.is_empty:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.queue.empty",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        tracks = list(player.queue)
        urls = [track.uri for track in tracks]
        info = await get_original_info(url=urls, track=track)
        message = "\n".join(
            f"{index}. *{track.title}*"
            for index, track in enumerate(tracks, start=1)
        )
        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.music.queue.list",
            queue=message,
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ))

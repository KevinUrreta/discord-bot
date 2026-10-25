import asyncio

import wavelink
from discord.ext import commands

from src.helpers import metadata
from src.helpers.embed import CustomEmbed


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

        info = await asyncio.gather(*(
            metadata.get_original_info(track.uri or "", track)
            for track in tracks
        ))

        message = "\n".join(
            f"{index}. *{data.get('title', 'Título desconocido')}*"
            for index, data in enumerate(info, start=1)
        )

        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.music.queue.list",
            queue=message,
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ))

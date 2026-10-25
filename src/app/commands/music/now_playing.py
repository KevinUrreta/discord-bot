import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed
from src.helpers.formatting import format_duration
from src.helpers.metadata import get_original_info


class NowPlaying(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="nowplaying", aliases=["now"])
    async def nowplaying(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.now_playing.not_connected",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        player: wavelink.Player = ctx.voice_client
        track = player.current

        if track is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.now_playing.now_playing_empty",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        data = await get_original_info(track.uri or "", track)

        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.music.now_playing.success",
            client=self.client,
            thumbnail=data.get("thumbnail"),
            url=track.uri or "",
            title=data.get("title", "Título desconocido"),
            duration=format_duration(track.length),
            views=data.get("views", "N/A"),
            queue=player.queue.count,
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ))

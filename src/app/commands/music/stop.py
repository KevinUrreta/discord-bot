import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed


class Stop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="stop")
    async def stop(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.stop.not_connected",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        player: wavelink.Player = ctx.voice_client
        player.autoplay = wavelink.AutoPlayMode.disabled

        if player.queue is not None:
            player.queue.clear()

            if hasattr(player.queue, "history") and player.queue.history is not None:
                try:
                    player.queue.history.clear()
                except AttributeError:
                    pass
        await player.stop()
        await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.stop.stopped",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))

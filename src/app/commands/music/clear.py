import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="clear")
    async def clear(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.clear.not_connected",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        player: wavelink.Player = ctx.voice_client

        if player.queue.is_empty:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.clear.empty",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        player.queue.clear()
        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.music.clear.cleared",
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ))

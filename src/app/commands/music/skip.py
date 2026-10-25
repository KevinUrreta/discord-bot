import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed


class Skip(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.skip.not_connected",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        player: wavelink.Player = ctx.voice_client

        if player.current is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.skip.no_song_playing",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        await player.skip(force=True)
        await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.skip.skipped",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))

import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed


class Resume(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="resume", aliases=["continue"])
    async def resume(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.resume.not_connected",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        player: wavelink.Player = ctx.voice_client
        if not player.paused:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.resume.no_song_playing",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        await player.pause(False)
        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.music.resume.success",
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ))

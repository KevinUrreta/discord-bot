import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed


class Pause(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="pause")
    async def pause(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.pause.not_connected",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        player: wavelink.Player = ctx.voice_client

        if not player.playing:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.pause.no_song_playing",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        await player.pause(True)
        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.music.pause.paused",
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ))

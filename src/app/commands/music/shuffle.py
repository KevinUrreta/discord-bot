import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed


class Shuffle(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="shuffle")
    async def shuffle(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.shuffle.not_connected",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        player: wavelink.Player = ctx.voice_client
        if player.queue.count < 2:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.shuffle.not_enough_songs",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        player.queue.shuffle()
        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.music.shuffle.shuffled",
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ))

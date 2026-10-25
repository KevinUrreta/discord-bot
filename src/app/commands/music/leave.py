from discord.ext import commands

from src.helpers.embed import CustomEmbed


class Leave(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="leave")
    async def leave(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.leave.not_connected",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        ctx.voice_client.disconnect()
        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.music.leave.disconnected",
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ))

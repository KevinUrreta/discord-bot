import wavelink
from discord.ext import commands


class Join(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="join")
    async def join(self, ctx):
        if ctx.author.voice is None:
            return

        channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await channel.connect(cls=wavelink.Player)
            return

        if ctx.voice_client.channel != channel:
            await ctx.voice_client.move_to(channel)

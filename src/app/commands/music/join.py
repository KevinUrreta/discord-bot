import wavelink
from discord.ext import commands


class Join(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="join")
    async def join(self, ctx):
        if not ctx.voice_client == ctx.author.voice:
            await ctx.author.voice.channel.connect(cls=wavelink.Player)

        if ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(ctx.author.voice.channel)

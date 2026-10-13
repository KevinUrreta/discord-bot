from discord.ext import commands

class Volume(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="volume", aliases=["vol"])
    async def volume(self, ctx: commands.Context, volume: int):
        if volume is None:
            await ctx.send("Volume is required.")
            return
        if volume < 1:
            await ctx.send("Volume must be greater than 0.")
            return
        if volume > 100:
            await ctx.send("Volume must be less than 100.")
            return

        await ctx.send(f"Volume: {volume}%")
from discord.ext import commands

from src.app.client import Client
from src.helpers.embed import CustomEmbed


class Ping(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        latency = round(self.client.latency * 1000)
        await ctx.send(
            embed=await CustomEmbed.create(
                ctx,
                key="app.commands.info.ping.response",
                latency=latency,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            )
        )

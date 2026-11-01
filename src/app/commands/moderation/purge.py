from discord.ext import commands
from src.helpers import permissions
from src.helpers.embed import CustomEmbed


class Purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @permissions.has_manage_messages()
    @commands.command(name="purge")
    async def purge(self, ctx, amount: int):
        if amount < 1:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.moderation.purge.invalid_amount",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.moderation.purge.success",
            amount=len(deleted),
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ), delete_after=5)

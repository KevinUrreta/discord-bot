from discord.ext import commands

from src.app.client import Client
from src.helpers import permissions
from src.helpers.embed import CustomEmbed
from src.infrastructure.database.repositories.guild_settings import GuildSettingsRepository


class Prefix(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @permissions.has_manage_guild()
    @commands.command(name="prefix")
    async def prefix(self, ctx: commands.Context, prefix: str | None = None) -> None:
        guild = ctx.guild
        if guild is None:
            return

        if prefix is not None and not 1 <= len(prefix) <= 10:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.info.prefix.invalid_prefix",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        repo = GuildSettingsRepository(self.client.db)
        settings = await repo.read(guild.id)
        if settings is None:
            settings = await repo.create(guild_id=guild.id)
        current = settings.prefix

        if prefix is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.info.prefix.current_prefix",
                prefix=current,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        await repo.update(guild.id, prefix=prefix)
        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.info.prefix.set_prefix",
            prefix=prefix,
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ))

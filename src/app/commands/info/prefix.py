from discord.ext import commands

from src.app.client import Client
from src.i18n.translate import i18n
from src.infrastructure.database.repositories.guild_settings import GuildSettingsRepository


class Prefix(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="prefix")
    async def prefix(self, ctx: commands.Context, prefix: str | None = None) -> None:
        guild = ctx.guild
        if guild is None:
            return

        repo = GuildSettingsRepository(self.client.db)
        settings = await repo.read(guild.id)
        current = settings.prefix

        if prefix is None:
            await ctx.send(await i18n(ctx, "app.commands.info.prefix.current_prefix", prefix=current))
            return

        await repo.update(guild.id, prefix=prefix)
        await ctx.send(await i18n(ctx, "app.commands.info.prefix.set_prefix", prefix=prefix))


import logging

import discord
from discord.ext import commands

from src.helpers.embed import CustomEmbed

logger = logging.getLogger("discord")


class OnCommandError(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    async def _send_error(self, ctx: commands.Context, key: str) -> None:
        try:
            embed = await CustomEmbed.create(
                ctx,
                key=key,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            )
            await ctx.send(embed=embed)
        except (discord.HTTPException, ValueError, TypeError):
            logger.exception(
                "Failed to send command error response for '%s'.",
                ctx.command.qualified_name if ctx.command else "unknown",
            )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError, ) -> None:
        # Unknown commands are ignored to avoid unnecessary chat messages.
        if isinstance(error, commands.CommandNotFound):
            return

        # Discord.py wraps exceptions raised inside a command.
        if isinstance(error, commands.CommandInvokeError):
            original = error.original
            logger.error(
                "Command '%s' failed unexpectedly.",
                ctx.command.qualified_name if ctx.command else "unknown",
                exc_info=(
                    type(original),
                    original,
                    original.__traceback__,
                ),
            )
            await self._send_error(ctx, "app.errors.command.unexpected", )
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await self._send_error(ctx, "app.errors.command.missing_argument", )
            return

        if isinstance(
            error,
            (
                commands.BadArgument,
                commands.BadUnionArgument,
                commands.BadLiteralArgument,
                commands.ConversionError,
            ),
        ):
            await self._send_error(ctx, "app.errors.command.invalid_argument", )
            return

        if isinstance(error, commands.BotMissingPermissions):
            await self._send_error(ctx, "app.errors.command.bot_missing_permissions", )
            return

        if isinstance(error, commands.MissingPermissions):
            await self._send_error(ctx, "app.errors.command.missing_permissions", )
            return

        if isinstance(error, commands.CommandOnCooldown):
            try:
                embed = await CustomEmbed.create(
                    ctx,
                    key="app.errors.command.cooldown",
                    seconds=f"{error.retry_after:.1f}",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
                await ctx.send(embed=embed)
            except (discord.HTTPException, ValueError, TypeError):
                logger.exception("Failed to send command cooldown response.")
            return

        if isinstance(error, commands.NoPrivateMessage):
            await self._send_error(ctx, "app.errors.command.guild_only", )
            return

        if isinstance(error, commands.CheckFailure):
            await self._send_error(ctx, "app.errors.command.check_failed", )
            return

        # Preserve visibility of any command errors not handled above.
        logger.error(
            "Unhandled command error in '%s': %s",
            ctx.command.qualified_name if ctx.command else "unknown",
            error,
            exc_info=(
                type(error),
                error,
                error.__traceback__,
            ),
        )
        await self._send_error(ctx, "app.errors.command.unexpected", )

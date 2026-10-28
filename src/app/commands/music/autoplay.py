from typing import cast

import wavelink
from discord.ext import commands

from src.app.client import Client
from src.helpers.embed import CustomEmbed
from src.infrastructure.database.repositories.guild_settings import GuildSettingsRepository


class AutoplayCommand(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="autoplay")
    async def autoplay(self, ctx: commands.Context, mode: str | None = None):
        guild = ctx.guild
        if guild is None:
            return

        repo = GuildSettingsRepository(self.client.db)
        settings = await repo.read(guild.id)
        if settings is None:
            settings = await repo.create(guild_id=guild.id)
        current_mode = settings.autoplay or "disabled"

        if mode is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.autoplay.current",
                mode=current_mode,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        mode_lower = mode.lower()
        if mode_lower in ["true", "enabled", "on"]:
            new_mode = "enabled"
        elif mode_lower in ["partial", "p"]:
            new_mode = "partial"
        elif mode_lower in ["false", "disabled", "off"]:
            new_mode = "disabled"
        else:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.autoplay.invalid",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        await repo.update(guild.id, autoplay=new_mode)

        if ctx.voice_client:
            player = cast(wavelink.Player, ctx.voice_client)
            if new_mode == "enabled":
                player.autoplay = wavelink.AutoPlayMode.enabled
            elif new_mode == "partial":
                player.autoplay = wavelink.AutoPlayMode.partial
            else:
                player.autoplay = wavelink.AutoPlayMode.disabled

        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.music.autoplay.updated",
            mode=new_mode,
            user=ctx.author.display_name,
            footer_icon=ctx.author.display_avatar.url
        ))

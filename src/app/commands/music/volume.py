from typing import cast

import wavelink
from discord.ext import commands

from src.app.client import Client
from src.helpers.embed import CustomEmbed
from src.infrastructure.database.repositories.guild_settings import GuildSettingsRepository


class Volume(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="volume", aliases=["vol"])
    async def volume(self, ctx: commands.Context, volume: int | None = None):
        guild = ctx.guild
        if guild is None:
            return

        repo = GuildSettingsRepository(self.client.db)
        settings = await repo.read(guild.id)
        current = settings.volume

        if volume is None:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.volume.current_volume",
                volume=current,
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        if not 1 <= volume <= 100:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.volume.invalid_volume",
                footer_icon=ctx.author.display_avatar.url
            ))
            return
        if ctx.voice_client is not None:
            player = cast(wavelink.Player, ctx.voice_client)
            await player.set_volume(volume)

        await repo.update(guild.id, volume=volume)
        await ctx.send(embed=await CustomEmbed.create(
            ctx,
            key="app.commands.music.volume.set_volume",
            volume=volume,
            footer_icon=ctx.author.display_avatar.url
        ))
        return

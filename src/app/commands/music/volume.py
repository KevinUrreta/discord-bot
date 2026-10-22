from typing import cast

import wavelink
from discord.ext import commands

from src.app.client import Client
from src.infrastructure.database.repositories.guild_settings import GuildSettingsRepository


class Volume(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="volume", aliases=["vol"])
    async def volume(self, ctx: commands.Context, volume: int | None = None) -> None:
        guild = ctx.guild
        if guild is None:
            return

        repo = GuildSettingsRepository(self.client.db)
        settings = await repo.read(ctx.guild.id)
        current = settings.volume if settings else 100

        if volume is None:
            await ctx.send(f"Volumen actual: {current}%")
            return

        if not 1 <= volume <= 100:
            await ctx.send("El volumen debe estar entre 1 y 100.")
            return

        if not isinstance(ctx.voice_client, wavelink.Player):
            await ctx.send("No estoy conectado a un canal de voz.")
            return

        if settings is None:
            await ctx.send("No se encontró la configuración de este servidor.")
            return

        await repo.update(guild.id, volume=volume)
        player = cast(wavelink.Player, ctx.voice_client)
        await player.set_volume(volume)
        await ctx.send(f"Volumen: {volume}%")

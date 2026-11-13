from typing import cast

import wavelink
from discord.ext import commands

from src.app.client import Client
from src.helpers.embed import CustomEmbed
from src.infrastructure.database.repositories.guild_settings import (
    GuildSettingsRepository,
)


class Volume(commands.Cog):
    """Componente que gestiona el volumen del reproductor de música.

    Permite a los usuarios modificar el nivel de volumen del audio
    reproducido en el servidor.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="volume", aliases=["vol"])
    async def volume(self, ctx: commands.Context, volume: int | None = None) -> None:
        """Muestra o ajusta el volumen del reproductor.

        Muestra el volumen actual si no se proporciona un valor,
        o establece el nuevo nivel (1-100).

        :param ctx: Contexto del comando de Discord.
        :param volume: Nivel de volumen entre 1 y 100.
        """
        guild = ctx.guild
        if guild is None:
            return

        repo = GuildSettingsRepository(self.client.db)
        settings = await repo.read(guild.id)

        if settings is None:
            settings = await repo.create(guild_id=guild.id)

        current = settings.volume

        if volume is None:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.volume.current_volume",
                    volume=current,
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return
        if not 1 <= volume <= 100:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.volume.invalid_volume",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return
        if ctx.voice_client is not None:
            player = cast(wavelink.Player, ctx.voice_client)
            await player.set_volume(volume)

        await repo.update(guild.id, volume=volume)
        await ctx.send(
            embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.volume.set_volume",
                volume=volume,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            )
        )
        return

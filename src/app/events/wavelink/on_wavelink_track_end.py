import asyncio
import logging

import discord
import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed

DELAY = 60
logger = logging.getLogger("discord")


class OnWavelinkTrackEnd(commands.Cog):
    """Gestiona el fin de las pistas y la inactividad del reproductor.

    Continúa la reproducción de la cola cuando corresponde y desconecta el
    reproductor tras un periodo de inactividad, notificando al canal asociado.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self, payload: wavelink.TrackEndEventPayload
    ) -> None:
        """Continúa la reproducción o desconecta al finalizar una pista.

        :param payload: Datos del evento de finalización de pista de Wavelink.
        """
        player: wavelink.Player | None = payload.player

        if player is None or player.channel is None:
            return

        # TODO: Revisar el algoritmo de recomendaciones de wavelink.
        # Actualmente, las recomendaciones pueden basarse en el historial
        # reciente y no priorizar las últimas canciones solicitadas.
        # Investigar si conviene utilizar las últimas tres canciones
        # solicitadas como referencias o, si no es viable, utilizar
        # la última canción solicitada como semilla de autoplay.
        # Mantener el comportamiento actual hasta evaluar la solución.
        # TODO: Revisar la gestión del fin de reproducción.
        # Comprobar el comportamiento de skip cuando el bucle está activado
        # y el autoplay desactivado, especialmente si la cola está vacía.
        # Evitar que queue.loaded se utilice incorrectamente después de
        # player.skip(force=True), ya que Wavelink puede establecerlo a None.
        # Verificar también que el autoplay no provoque reproducciones o
        # mensajes de recomendaciones duplicados.

        guild = player.channel.guild

        stop_requested = getattr(player, "stop_requested", False)

        if stop_requested:
            player.stop_requested = False

        if not stop_requested and player.autoplay != wavelink.AutoPlayMode.disabled:
            return

        queue = player.queue

        if not stop_requested and queue.mode == wavelink.QueueMode.loop:
            if queue.loaded is not None and not player.playing:
                await player.play(queue.get())
                return

            if queue.loaded is None and queue.is_empty:
                queue.mode = wavelink.QueueMode.normal

        if not stop_requested and not queue.is_empty and not player.playing:
            await player.play(queue.get())
            return

        if queue.is_empty and queue.mode == wavelink.QueueMode.normal:
            text_channel = getattr(player, "home", None)

            await asyncio.sleep(DELAY)

            if (
                player.channel is None
                or player.playing
                or player.current is not None
                or not player.queue.is_empty
                or player.queue.mode != wavelink.QueueMode.normal
            ):
                return

            await player.disconnect()

            if text_channel is None or not isinstance(
                text_channel, discord.abc.Messageable
            ):
                return

            await text_channel.send(
                embed=await CustomEmbed.create(
                    guild,
                    key="app.events.wavelink.idle_disconnect",
                    client=self.client,
                )
            )

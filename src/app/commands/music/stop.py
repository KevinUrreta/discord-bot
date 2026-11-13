import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed


class Stop(commands.Cog):
    """Componente que detiene la reproducción de música en el servidor.

    Permite a los usuarios detener la reproducción actual y limpiar la cola
    de reproducción dentro de la comunidad.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(name="stop")
    async def stop(self, ctx):
        """Detiene la reproducción y limpia la cola de reproducción.

        Detiene completamente el reproductor y elimina todas las pistas pendientes.

        :param ctx: Contexto del comando de Discord.
        """
        if ctx.voice_client is None:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.stop.not_connected",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return

        player: wavelink.Player = ctx.voice_client
        player.autoplay = wavelink.AutoPlayMode.disabled
        player.stop_requested = player.current is not None

        player.queue.reset()

        await player.stop()

        await ctx.send(
            embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.stop.stopped",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            )
        )

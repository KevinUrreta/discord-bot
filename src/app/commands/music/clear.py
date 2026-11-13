import wavelink
from discord.ext import commands

from src.app.client import Client
from src.helpers.embed import CustomEmbed


class Clear(commands.Cog):
    """Componente que vacía la cola de reproducción del bot en Discord.

    Permite a los usuarios eliminar todas las pistas de la cola de reproducción actual.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="clear")
    async def clear(self, ctx):
        """Vacía completamente la cola de reproducción del canal actual.

        Elimina todas las pistas pendientes de reproducción sin detener la pista actual.

        :param ctx: Contexto del comando de Discord.
        """
        if ctx.voice_client is None:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.clear.not_connected",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return
        player: wavelink.Player = ctx.voice_client

        if player.queue.is_empty:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.clear.empty",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return
        player.queue.clear()
        await ctx.send(
            embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.clear.cleared",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            )
        )

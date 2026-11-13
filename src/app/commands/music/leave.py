from discord.ext import commands

from src.app.client import Client
from src.helpers.embed import CustomEmbed


class Leave(commands.Cog):
    """Componente que permite desconectar al bot de un canal de voz en Discord.

    Permite a los administradores finalizar la conexión del bot desde el canal de voz actual.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="leave")
    async def leave(self, ctx):
        """Desconecta al bot del canal de voz actual y cierra la conexión.

        Detiene cualquier reproducción en curso y cierra la conexión con el canal.

        :param ctx: Contexto del comando de Discord.
        """
        if ctx.voice_client is None:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.leave.not_connected",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return

        await ctx.voice_client.disconnect()

        await ctx.send(
            embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.leave.disconnected",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            )
        )

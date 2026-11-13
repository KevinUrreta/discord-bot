from discord.ext import commands

from src.app.client import Client
from src.helpers.embed import CustomEmbed


class Ping(commands.Cog):
    """Componente que verifica la latencia del bot con Discord.

    Permite a los usuarios consultar el tiempo de respuesta del bot
    ante los comandos dentro del servidor.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """Muestra la latencia en la conexión a Discord Gateway.

        :param ctx: Contexto del comando de Discord.
        """

        latency = round(self.client.latency * 1000)
        await ctx.send(
            embed=await CustomEmbed.create(
                ctx,
                key="app.commands.info.ping.response",
                latency=latency,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            )
        )

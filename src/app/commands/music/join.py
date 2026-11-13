import wavelink
from discord.ext import commands

from src.app.client import Client


class Join(commands.Cog):
    """Componente que permite conectar al bot a un canal de voz.

    Permite a los usuarios invitar al bot al canal de voz donde se encuentran.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="join")
    async def join(self, ctx):
        """Conecta al bot al canal de voz del autor del comando.

        Mueve al bot al canal de voz actual del usuario si ya está conectado a otro.

        :param ctx: Contexto del comando de Discord.
        """
        if ctx.author.voice is None:
            return

        channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await channel.connect(cls=wavelink.Player)
            return

        if ctx.voice_client.channel != channel:
            await ctx.voice_client.move_to(channel)

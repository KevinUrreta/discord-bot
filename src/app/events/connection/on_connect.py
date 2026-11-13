import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnConnect(commands.Cog):
    """Registra que el bot estableció conexión con los servidores de Discord.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_connect(self):
        """Registra que se estableció correctamente la conexión con los servidores de Discord.
        """
        logger.info("Successful connection established with Discord servers")

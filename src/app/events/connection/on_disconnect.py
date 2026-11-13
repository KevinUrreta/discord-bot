import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnDisconnect(commands.Cog):
    """Registra la desconexión del bot de Discord.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_disconnect(self):
        """Registra que el bot se desconectó de Discord.
        """
        logger.info("The bot has disconnected from Discord")

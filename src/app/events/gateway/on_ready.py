import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnReady(commands.Cog):
    """Registra que el bot terminó de inicializarse y está listo para operar.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """Registra que el bot se inicializó correctamente y está listo para operar.
        """
        logger.info("Bot initialized successfully and ready to operate")

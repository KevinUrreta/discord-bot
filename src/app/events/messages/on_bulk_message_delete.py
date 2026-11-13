import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnBulkMessageDelete(commands.Cog):
    """Registra la cantidad de mensajes eliminados en bloque y el canal afectado.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        """Registra la cantidad de mensajes eliminados en bloque y el canal correspondiente.

        :param messages: Mensajes eliminados en bloque.
        """
        logger.info(
            f"Bulk deleted {len(messages)} messages in channel #{messages[0].channel if messages else 'unknown'}"
        )

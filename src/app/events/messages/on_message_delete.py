import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnMessageDelete(commands.Cog):
    """Registra el autor, canal y contenido de cada mensaje eliminado.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Registra el autor, el canal y el contenido del mensaje eliminado.

        :param message: Mensaje afectado por el evento.
        """
        logger.info(
            f'Message by {message.author} deleted in #{message.channel}: "{message.content}"'
        )

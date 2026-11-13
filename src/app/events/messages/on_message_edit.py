import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnMessageEdit(commands.Cog):
    """Registra los cambios de contenido de mensajes e ignora ediciones sin cambios de texto.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Registra los cambios de contenido de un mensaje e ignora las ediciones sin cambios de texto.

        :param before: Estado del objeto antes de la actualización.
        :param after: Estado del objeto después de la actualización.
        """
        if before.content == after.content:
            return
        logger.info(
            f"Message edited by {before.author} in #{before.channel}:"
            f'"{before.content}" -> "{after.content}"'
        )

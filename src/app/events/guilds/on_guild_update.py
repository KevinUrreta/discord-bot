import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildUpdate(commands.Cog):
    """Registra las actualizaciones de los ajustes del servidor.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """Registra la actualización de los ajustes del servidor.

        :param before: Estado del objeto antes de la actualización.
        :param after: Estado del objeto después de la actualización.
        """
        logger.info(f'Server settings for "{after.name}" (ID: {after.id}) were updated')

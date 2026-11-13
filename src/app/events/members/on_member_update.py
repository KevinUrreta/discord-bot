import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnMemberUpdate(commands.Cog):
    """Registra los cambios en el perfil o los roles de una persona del servidor.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Registra la actualización del perfil o los roles de un miembro.

        :param before: Estado del objeto antes de la actualización.
        :param after: Estado del objeto después de la actualización.
        """
        logger.info(f"Member profile or roles updated for {after} (ID: {after.id})")

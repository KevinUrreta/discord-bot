import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildChannelUpdate(commands.Cog):
    """Registra cambios de permisos o ajustes en canales del servidor.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        """Registra la actualización de permisos o ajustes de un canal del servidor.

        :param before: Estado del objeto antes de la actualización.
        :param after: Estado del objeto después de la actualización.
        """
        logger.info(
            f'Channel updated: "{after.name}" (ID: {after.id}) in "{after.guild.name}" | Permissions or settings changed'
        )

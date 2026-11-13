import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildRoleUpdate(commands.Cog):
    """Registra los cambios en roles del servidor.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        """Registra la actualización de un rol del servidor.

        :param before: Estado del objeto antes de la actualización.
        :param after: Estado del objeto después de la actualización.
        """
        logger.info(
            f'Role updated: "{after.name}" (ID: {after.id}) in "{after.guild.name}"'
        )

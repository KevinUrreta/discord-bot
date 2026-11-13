import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildRoleDelete(commands.Cog):
    """Registra la eliminaci?n de roles del servidor y el servidor afectado.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Registra el rol eliminado y el servidor del que se retiró.

        :param role: Rol afectado por el evento.
        """
        logger.info(
            f'Role deleted: "{role.name}" (ID: {role.id}) from "{role.guild.name}"'
        )

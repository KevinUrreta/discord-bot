import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildRoleCreate(commands.Cog):
    """Registra la creaci?n de roles del servidor, incluido su nombre, color e identificador.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Registra el rol creado, su color y el servidor al que pertenece.

        :param role: Rol afectado por el evento.
        """
        logger.info(
            f'Role created: "{role.name}" (ID: {role.id}) with color {role.color} in "{role.guild.name}"'
        )

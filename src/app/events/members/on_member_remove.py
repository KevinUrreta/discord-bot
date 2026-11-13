import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnMemberRemove(commands.Cog):
    """Registra cuándo una persona sale de un servidor o es expulsada.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Registra la salida o expulsión de un miembro del servidor.

        :param member: Miembro afectado por el evento.
        """
        logger.info(
            f'Member left or was kicked: {member} (ID: {member.id}) from "{member.guild.name}"'
        )

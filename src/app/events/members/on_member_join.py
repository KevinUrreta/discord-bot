import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnMemberJoin(commands.Cog):
    """Registra la incorporación de una persona a un servidor.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Registra la incorporación de un miembro al servidor.

        :param member: Miembro afectado por el evento.
        """
        logger.info(
            f'New member joined: {member} (ID: {member.id}) to server "{member.guild.name}"'
        )

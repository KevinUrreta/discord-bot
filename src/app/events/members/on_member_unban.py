import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnMemberUnban(commands.Cog):
    """Registra cuándo se levanta la prohibición de acceso de un usuario.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """Registra el levantamiento de la prohibición de un usuario en el servidor.

        :param guild: Servidor al que corresponde el evento.
        :param user: Usuario al que corresponde el evento.
        """
        logger.info(f'User unbanned: {user} (ID: {user.id}) in server "{guild.name}"')

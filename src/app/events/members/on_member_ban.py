import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnMemberBan(commands.Cog):
    """Registra cuándo se prohíbe a un usuario acceder a un servidor.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Registra el usuario expulsado mediante una prohibición y el servidor correspondiente.

        :param guild: Servidor al que corresponde el evento.
        :param user: Usuario al que corresponde el evento.
        """
        logger.info(f'User banned: {user} (ID: {user.id}) from server "{guild.name}"')

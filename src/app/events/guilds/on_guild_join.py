import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildJoin(commands.Cog):
    """Registra la incorporación del bot a un servidor, incluido su propietario y cantidad de miembros.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Registra la incorporación del bot a un servidor, con su nombre, identificador, propietario y cantidad de miembros.

        :param guild: Servidor al que corresponde el evento.
        """
        logger.info(
            f'The bot joined server: "{guild.name}" (ID: {guild.id}, Owner: {guild.owner}, Members: {guild.member_count})'
        )

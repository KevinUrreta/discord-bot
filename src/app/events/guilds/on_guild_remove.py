import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildRemove(commands.Cog):
    """Registra cuándo el bot abandona un servidor o es retirado de él.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Registra que el bot fue retirado de un servidor o lo abandonó.

        :param guild: Servidor al que corresponde el evento.
        """
        logger.info(
            f'The bot was removed from or left server: "{guild.name}" (ID: {guild.id})'
        )

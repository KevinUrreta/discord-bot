import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildChannelDelete(commands.Cog):
    """Registra la eliminación de canales del servidor con su nombre e identificador.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Registra el nombre y el identificador del canal eliminado, junto con su servidor.

        :param channel: Canal del servidor afectado por el evento.
        """
        logger.info(
            f'Channel deleted: "{channel.name}" (ID: {channel.id}) in server "{channel.guild.name}"'
        )

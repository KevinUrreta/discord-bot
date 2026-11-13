import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildChannelCreate(commands.Cog):
    """Registra la creación de canales del servidor con su nombre, tipo e identificador.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Registra el nombre, el tipo y el identificador del canal creado, junto con su servidor.

        :param channel: Canal del servidor afectado por el evento.
        """
        logger.info(
            f'Channel created: "{channel.name}" (Type: {channel.type}) in server "{channel.guild.name}" (ID: {channel.id})'
        )

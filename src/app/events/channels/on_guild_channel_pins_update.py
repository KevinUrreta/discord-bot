import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildChannelPinsUpdate(commands.Cog):
    """Registra los cambios en los mensajes fijados de un canal del servidor.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        """Registra la actualización de los mensajes fijados en un canal del servidor.

        :param channel: Canal del servidor afectado por el evento.
        :param last_pin: Fecha y hora del mensaje fijado más recientemente.
        """
        logger.info(f'Pins updated in channel "{channel.name}" (ID: {channel.id})')

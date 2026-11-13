import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnPrivateChannelPinsUpdate(commands.Cog):
    """Registra las actualizaciones de mensajes fijados en canales privados y los datos del evento.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_private_channel_pins_update(self, *args, **kwargs):
        """Registra la activación del evento y los argumentos recibidos.

        :param args: Argumentos posicionales recibidos con el evento.
        :param kwargs: Argumentos con nombre recibidos con el evento.
        """
        logger.info(
            f"Event on_private_channel_pins_update triggered with args={args}, kwargs={kwargs}"
        )

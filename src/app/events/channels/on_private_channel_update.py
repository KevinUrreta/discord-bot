import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnPrivateChannelUpdate(commands.Cog):
    """Registra las actualizaciones de canales privados y los datos del evento.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_private_channel_update(self, *args, **kwargs):
        """Registra la activación del evento y los argumentos recibidos.

        :param args: Argumentos posicionales recibidos con el evento.
        :param kwargs: Argumentos con nombre recibidos con el evento.
        """
        logger.info(
            f"Event on_private_channel_update triggered with args={args}, kwargs={kwargs}"
        )

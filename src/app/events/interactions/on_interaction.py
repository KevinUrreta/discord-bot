import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnInteraction(commands.Cog):
    """Registra las interacciones recibidas por Discord y los datos asociados.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_interaction(self, *args, **kwargs):
        """Registra la activación del evento y los argumentos recibidos.

        :param args: Argumentos posicionales recibidos con el evento.
        :param kwargs: Argumentos con nombre recibidos con el evento.
        """
        logger.info(f"Event on_interaction triggered with args={args}, kwargs={kwargs}")

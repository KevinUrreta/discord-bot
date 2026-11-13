import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildAvailable(commands.Cog):
    """Registra cuándo Discord marca un servidor como disponible.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_available(self, *args, **kwargs):
        """Registra la activación del evento y los argumentos recibidos.

        :param args: Argumentos posicionales recibidos con el evento.
        :param kwargs: Argumentos con nombre recibidos con el evento.
        """
        logger.info(
            f"Event on_guild_available triggered with args={args}, kwargs={kwargs}"
        )

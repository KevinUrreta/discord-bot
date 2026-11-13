import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildEmojisUpdate(commands.Cog):
    """Registra las actualizaciones de emojis del servidor y los datos del evento.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, *args, **kwargs):
        """Registra la activación del evento y los argumentos recibidos.

        :param args: Argumentos posicionales recibidos con el evento.
        :param kwargs: Argumentos con nombre recibidos con el evento.
        """
        logger.info(
            f"Event on_guild_emojis_update triggered with args={args}, kwargs={kwargs}"
        )

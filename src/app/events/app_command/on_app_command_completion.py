import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnAppCommandCompletion(commands.Cog):
    """Registra la finalización de comandos de aplicación y los datos asociados.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_app_command_completion(self, *args, **kwargs):
        """Registra la activación del evento y los argumentos recibidos.

        :param args: Argumentos posicionales recibidos con el evento.
        :param kwargs: Argumentos con nombre recibidos con el evento.
        """
        logger.info(
            f"Event on_app_command_completion triggered with args={args}, kwargs={kwargs}"
        )

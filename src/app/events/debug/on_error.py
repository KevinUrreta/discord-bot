import logging
import sys

from discord.ext import commands

logger = logging.getLogger("discord")


class OnError(commands.Cog):
    """Registra las excepciones no controladas junto con el evento en el que ocurrieron.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_error(self, event_method: str, *args, **kwargs) -> None:
        """Registra la excepción no controlada junto con el nombre del evento en el que ocurrió.

        :param event_method: Nombre del método del evento en el que ocurrió la excepción.
        """
        logger.error(
            "Unhandled exception in event %s",
            event_method,
            exc_info=sys.exc_info(),
        )

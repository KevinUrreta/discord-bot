import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnReactionClearEmoji(commands.Cog):
    """Registra cu?ndo se eliminan de un mensaje las reacciones de un emoji.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_clear_emoji(self, *args, **kwargs):
        """Registra la activación del evento y los argumentos recibidos.

        :param args: Argumentos posicionales recibidos con el evento.
        :param kwargs: Argumentos con nombre recibidos con el evento.
        """
        logger.info(
            f"Event on_reaction_clear_emoji triggered with args={args}, kwargs={kwargs}"
        )

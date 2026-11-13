import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnInviteCreate(commands.Cog):
    """Registra la creación de invitaciones y los datos recibidos.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_invite_create(self, *args, **kwargs):
        """Registra la activación del evento y los argumentos recibidos.

        :param args: Argumentos posicionales recibidos con el evento.
        :param kwargs: Argumentos con nombre recibidos con el evento.
        """
        logger.info(
            f"Event on_invite_create triggered with args={args}, kwargs={kwargs}"
        )

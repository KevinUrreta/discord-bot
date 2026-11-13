import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnAuditLogEntryCreate(commands.Cog):
    """Registra la creación de entradas en el registro de auditoría y sus datos.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, *args, **kwargs):
        """Registra la activación del evento y los argumentos recibidos.

        :param args: Argumentos posicionales recibidos con el evento.
        :param kwargs: Argumentos con nombre recibidos con el evento.
        """
        logger.info(
            f"Event on_audit_log_entry_create triggered with args={args}, kwargs={kwargs}"
        )

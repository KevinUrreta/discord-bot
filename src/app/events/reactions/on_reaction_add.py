import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnReactionAdd(commands.Cog):
    """Registra las reacciones a?adidas, qui?n las a?ade y el mensaje correspondiente.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Registra la reacción añadida, quién la añadió y el mensaje asociado.

        :param reaction: Reacción afectada por el evento.
        :param user: Usuario al que corresponde el evento.
        """
        logger.info(
            f"Reaction {reaction.emoji} added by {user} to message ID {reaction.message.id}"
        )

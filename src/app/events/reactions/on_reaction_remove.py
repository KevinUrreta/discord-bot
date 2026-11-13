import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnReactionRemove(commands.Cog):
    """Registra las reacciones retiradas, qui?n las retira y el mensaje correspondiente.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        """Registra la reacción retirada, quién la retiró y el mensaje asociado.

        :param reaction: Reacción afectada por el evento.
        :param user: Usuario al que corresponde el evento.
        """
        logger.info(
            f"Reaction {reaction.emoji} removed by {user} from message ID {reaction.message.id}"
        )

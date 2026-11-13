import logging

from discord.ext import commands

logger = logging.getLogger("discord")


class OnVoiceChannelEffect(commands.Cog):
    """Registra la reproducción de un efecto de sonido y el identificador del canal de voz.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_channel_effect(self, effect):
        """Registra la reproducción de un efecto de sonido y el identificador del canal.

        :param effect: Efecto de sonido reproducido en un canal de voz.
        """
        logger.info(
            f"Soundboard effect played in channel ID: {getattr(effect, 'channel_id', 'N/A')}"
            'by user ID: {getattr(effect, "user_id", "N/A")}'
        )

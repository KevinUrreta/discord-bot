import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnVoiceChannelEffect(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_channel_effect(self, effect):
        logger.info(
            f'Soundboard effect played in channel ID: {getattr(effect , "channel_id" , "N/A")}'
            'by user ID: {getattr(effect, "user_id", "N/A")}'
            )

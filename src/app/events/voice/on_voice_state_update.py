import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnVoiceStateUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        logger.info(f"Voice state updated for {member}: left \"{before.channel}\" and joined \"{after.channel}\"")

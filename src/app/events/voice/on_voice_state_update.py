import logging

import wavelink
from discord.ext import commands

logger = logging.getLogger("discord")


class OnVoiceStateUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        logger.info(f"Voice state updated for {member}: left \"{before.channel}\" and joined \"{after.channel}\"")

        channel = before.channel
        if channel is None:
            return

        player = member.guild.voice_client
        if player is None or player.channel != channel:
            return

        if any(not voice_member.bot for voice_member in channel.members):
            return

        player.autoplay = wavelink.AutoPlayMode.disabled
        await player.disconnect()

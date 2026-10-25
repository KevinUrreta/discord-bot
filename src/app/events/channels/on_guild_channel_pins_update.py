import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildChannelPinsUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        logger.info(f"Pins updated in channel \"{channel.name}\" (ID: {channel.id})")

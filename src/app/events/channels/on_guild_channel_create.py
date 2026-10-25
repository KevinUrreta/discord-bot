import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildChannelCreate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        logger.info(f"Channel created: \"{channel.name}\" (Type: {channel.type}) in server \"{channel.guild.name}\" (ID: {channel.id})")

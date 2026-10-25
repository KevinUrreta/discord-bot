import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildChannelUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        logger.info(f"Channel updated: \"{after.name}\" (ID: {after.id}) in \"{after.guild.name}\" | Permissions or settings changed")

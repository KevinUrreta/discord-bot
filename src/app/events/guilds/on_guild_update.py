import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        logger.info(f"Server settings for \"{after.name}\" (ID: {after.id}) were updated")

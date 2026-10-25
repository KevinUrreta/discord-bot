import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        logger.info(f"The bot was removed from or left server: \"{guild.name}\" (ID: {guild.id})")

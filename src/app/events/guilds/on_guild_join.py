import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logger.info(f"The bot joined server: \"{guild.name}\" (ID: {guild.id}, Owner: {guild.owner}, Members: {guild.member_count})")

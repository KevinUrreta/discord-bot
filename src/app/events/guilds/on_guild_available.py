import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildAvailable(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_available(self, *args, **kwargs):
        logger.info(f"Event on_guild_available triggered with args={args}, kwargs={kwargs}")

import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildUnavailable(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_unavailable(self, *args, **kwargs):
        logger.info(f"Event on_guild_unavailable triggered with args={args}, kwargs={kwargs}")

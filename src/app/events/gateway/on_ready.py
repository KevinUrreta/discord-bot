import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Bot initialized successfully and ready to operate")

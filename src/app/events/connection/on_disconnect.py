import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnDisconnect(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_disconnect(self):
        logger.info(f"The bot has disconnected from Discord")

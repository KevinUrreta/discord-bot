import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnConnect(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_connect(self):
        logger.info(f"Successful connection established with Discord servers")

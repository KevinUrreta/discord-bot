import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnError(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_error(self, *args, **kwargs):
        logger.info(f"Event on_error triggered with args={args}, kwargs={kwargs}")

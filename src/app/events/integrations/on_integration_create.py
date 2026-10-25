import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnIntegrationCreate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_integration_create(self, *args, **kwargs):
        logger.info(f"Event on_integration_create triggered with args={args}, kwargs={kwargs}")

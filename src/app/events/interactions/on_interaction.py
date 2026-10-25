import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnInteraction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_interaction(self, *args, **kwargs):
        logger.info(f"Event on_interaction triggered with args={args}, kwargs={kwargs}")

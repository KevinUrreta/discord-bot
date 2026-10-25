import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnThreadRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_thread_remove(self, *args, **kwargs):
        logger.info(f"Event on_thread_remove triggered with args={args}, kwargs={kwargs}")

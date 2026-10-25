import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnThreadDelete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        logger.info(f"Thread deleted: \"{thread.name}\" (ID: {thread.id})")

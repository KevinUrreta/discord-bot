import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnThreadCreate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        logger.info(f"Thread created: \"{thread.name}\" (ID: {thread.id}) in #{thread.parent}")

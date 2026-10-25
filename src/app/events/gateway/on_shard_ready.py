import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnShardReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_shard_ready(self, *args, **kwargs):
        logger.info(f"Event on_shard_ready triggered with args={args}, kwargs={kwargs}")

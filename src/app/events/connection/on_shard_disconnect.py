import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnShardDisconnect(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_shard_disconnect(self, *args, **kwargs):
        logger.info(f"Event on_shard_disconnect triggered with args={args}, kwargs={kwargs}")

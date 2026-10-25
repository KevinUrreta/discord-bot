import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnShardConnect(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_shard_connect(self, *args, **kwargs):
        logger.info(f"Event on_shard_connect triggered with args={args}, kwargs={kwargs}")

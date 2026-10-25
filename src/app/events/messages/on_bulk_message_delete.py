import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnBulkMessageDelete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        logger.info(f"Bulk deleted {len(messages)} messages in channel #{messages[0].channel if messages else 'unknown'}")

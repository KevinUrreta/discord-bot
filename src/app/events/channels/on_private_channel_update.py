import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnPrivateChannelUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_private_channel_update(self, *args, **kwargs):
        logger.info(f"Event on_private_channel_update triggered with args={args}, kwargs={kwargs}")

import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnSubscriptionUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_subscription_update(self, *args, **kwargs):
        logger.info(f"Event on_subscription_update triggered with args={args}, kwargs={kwargs}")

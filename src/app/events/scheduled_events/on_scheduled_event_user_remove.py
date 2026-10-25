import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnScheduledEventUserRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_scheduled_event_user_remove(self, *args, **kwargs):
        logger.info(f"Event on_scheduled_event_user_remove triggered with args={args}, kwargs={kwargs}")

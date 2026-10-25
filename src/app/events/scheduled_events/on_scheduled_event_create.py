import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnScheduledEventCreate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_scheduled_event_create(self, *args, **kwargs):
        logger.info(f"Event on_scheduled_event_create triggered with args={args}, kwargs={kwargs}")

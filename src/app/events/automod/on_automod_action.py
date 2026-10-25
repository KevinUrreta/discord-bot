import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnAutomodAction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_automod_action(self, *args, **kwargs):
        logger.info(f"Event on_automod_action triggered with args={args}, kwargs={kwargs}")

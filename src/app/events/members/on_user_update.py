import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnUserUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_user_update(self, *args, **kwargs):
        logger.info(f"Event on_user_update triggered with args={args}, kwargs={kwargs}")

import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnTyping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_typing(self, *args, **kwargs):
        logger.info(f"Event on_typing triggered with args={args}, kwargs={kwargs}")

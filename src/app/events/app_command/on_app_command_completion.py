import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnAppCommandCompletion(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_app_command_completion(self, *args, **kwargs):
        logger.info(f"Event on_app_command_completion triggered with args={args}, kwargs={kwargs}")

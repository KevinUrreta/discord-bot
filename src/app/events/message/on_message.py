import logging

from discord.ext import commands

logger = logging.getLogger("discord")

class OnMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        logger.info(f"{message.author.name}: {message.content}")

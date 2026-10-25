import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnMessageDelete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        logger.info(f"Message by {message.author} deleted in #{message.channel}: \"{message.content}\"")

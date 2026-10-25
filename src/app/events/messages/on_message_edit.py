import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnMessageEdit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return
        logger.info(
            f"Message edited by {before.author} in #{before.channel}:"
            f"\"{before.content}\" -> \"{after.content}\""
        )

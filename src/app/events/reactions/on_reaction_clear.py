import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnReactionClear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_clear(self, *args, **kwargs):
        logger.info(f"Event on_reaction_clear triggered with args={args}, kwargs={kwargs}")

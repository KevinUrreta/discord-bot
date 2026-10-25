import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnReactionClearEmoji(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_clear_emoji(self, *args, **kwargs):
        logger.info(f"Event on_reaction_clear_emoji triggered with args={args}, kwargs={kwargs}")

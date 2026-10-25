import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnReactionAdd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        logger.info(f"Reaction {reaction.emoji} added by {user} to message ID {reaction.message.id}")

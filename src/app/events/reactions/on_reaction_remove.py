import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnReactionRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        logger.info(f"Reaction {reaction.emoji} removed by {user} from message ID {reaction.message.id}")

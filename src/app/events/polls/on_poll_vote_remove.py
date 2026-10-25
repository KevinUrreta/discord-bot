import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnPollVoteRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_poll_vote_remove(self, *args, **kwargs):
        logger.info(f"Event on_poll_vote_remove triggered with args={args}, kwargs={kwargs}")

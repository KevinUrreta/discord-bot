import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnThreadMemberJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_thread_member_join(self, *args, **kwargs):
        logger.info(f"Event on_thread_member_join triggered with args={args}, kwargs={kwargs}")

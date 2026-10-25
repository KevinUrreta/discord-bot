import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnMemberUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        logger.info(f"Member profile or roles updated for {after} (ID: {after.id})")

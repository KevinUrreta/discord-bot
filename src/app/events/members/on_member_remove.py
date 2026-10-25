import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnMemberRemove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logger.info(f"Member left or was kicked: {member} (ID: {member.id}) from \"{member.guild.name}\"")

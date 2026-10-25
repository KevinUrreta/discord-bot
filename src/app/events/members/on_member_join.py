import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnMemberJoin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        logger.info(f"New member joined: {member} (ID: {member.id}) to server \"{member.guild.name}\"")

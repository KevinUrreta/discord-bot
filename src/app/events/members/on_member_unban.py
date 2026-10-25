import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnMemberUnban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        logger.info(f"User unbanned: {user} (ID: {user.id}) in server \"{guild.name}\"")

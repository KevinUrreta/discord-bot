import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnMemberBan(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        logger.info(f"User banned: {user} (ID: {user.id}) from server \"{guild.name}\"")

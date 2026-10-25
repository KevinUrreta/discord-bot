import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildRoleUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        logger.info(f"Role updated: \"{after.name}\" (ID: {after.id}) in \"{after.guild.name}\"")

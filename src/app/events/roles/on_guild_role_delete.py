import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildRoleDelete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        logger.info(f"Role deleted: \"{role.name}\" (ID: {role.id}) from \"{role.guild.name}\"")

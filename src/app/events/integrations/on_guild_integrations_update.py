import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnGuildIntegrationsUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_integrations_update(self, *args, **kwargs):
        logger.info(f"Event on_guild_integrations_update triggered with args={args}, kwargs={kwargs}")

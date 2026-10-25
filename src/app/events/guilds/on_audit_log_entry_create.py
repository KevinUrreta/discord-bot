import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnAuditLogEntryCreate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, *args, **kwargs):
        logger.info(f"Event on_audit_log_entry_create triggered with args={args}, kwargs={kwargs}")

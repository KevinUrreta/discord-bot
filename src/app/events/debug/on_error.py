import logging
import sys

from discord.ext import commands

logger = logging.getLogger("discord")


class OnError(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_error(self, event_method: str, *args, **kwargs) -> None:
        logger.error(
            "Unhandled exception in event %s",
            event_method,
            exc_info=sys.exc_info(),
        )

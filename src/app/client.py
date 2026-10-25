import logging

import discord
from discord.ext import commands

from src.core.config import Settings
from src.core.loader import load_module
from src.helpers.prefix import get_prefix
from src.infrastructure.database.connection import Database
from src.infrastructure.lavalink.connection import Lavalink

logger = logging.getLogger("discord")


class Client(commands.Bot):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.db = Database(url=settings.postgres_url)

        super().__init__(
            command_prefix=get_prefix,
            intents=discord.Intents.all(),
            enable_debug_events=True,
        )

    async def setup_hook(self) -> None:
        await self.db.create_tables()
        await load_module(self)
        await Lavalink.connect_lavalink(self)

    async def close(self) -> None:
        try:
            await super().close()
        finally:
            await self.db.close()

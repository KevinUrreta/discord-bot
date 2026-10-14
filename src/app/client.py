import discord
from discord.ext import commands

from src.core.loader import load_module
from src.infrastructure.lavalink.connection import Lavalink

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await load_module(self)
        await Lavalink.connect_lavalink(self)
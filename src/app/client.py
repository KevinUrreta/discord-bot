import discord
from discord.ext import commands

from src.core.loader import load_module


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await load_module(self)
import logging
from discord.ext import commands

logger = logging.getLogger("discord")


class OnSoundboardSoundCreate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_soundboard_sound_create(self, *args, **kwargs):
        logger.info(f"Event on_soundboard_sound_create triggered with args={args}, kwargs={kwargs}")

from typing import Optional, cast

import wavelink
from discord.ext import commands

from src.app.client import Client
from src.infrastructure.database.repositories.guild import GuildRepository


class Volume(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.command(name="volume", aliases=["vol"])
    async def volume(self, ctx: commands.Context, volume: Optional[int] = None):
        guild = ctx.guild
        if guild is None:
            return

        await self.client.db.connect()
        try:
            guild_repo = GuildRepository(self.client.db)

            if volume is None:
                guild_db = await guild_repo.get(guild.id)
                current_volume = (
                    guild_db.settings.volume
                    if guild_db and guild_db.settings else 100
                )

                await ctx.send(f"Actual volume: {current_volume}%")
                return

            if ctx.voice_client is None:
                await ctx.send("Not connected to a voice channel.")
                return
            if volume < 1:
                await ctx.send("Volume must be greater than 0.")
                return
            if volume > 100:
                await ctx.send("Volume must be less than 100.")
                return

            server = await guild_repo.create_or_update(guild_id=guild.id, name=guild.name)

            if server and server.settings:
                server.settings.volume = volume
                async with self.client.db.get_session() as session:
                    db_guild = await session.merge(server)
                    db_guild.settings.volume = volume
                    await session.commit()

            player = cast(wavelink.Player, ctx.voice_client)
            await player.set_volume(volume)

            await ctx.send(f"Volume: {volume}%")
        finally:
            await self.client.db.close()
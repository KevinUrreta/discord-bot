import asyncio
import logging

import discord
import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed

DELAY = 60
logger = logging.getLogger("discord")


class OnWavelinkTrackEnd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player or not player.channel:
            return
        guild: discord.Guild = player.channel.guild

        if getattr(player, "autoplay", wavelink.AutoPlayMode.disabled) != wavelink.AutoPlayMode.disabled:
            return

        if player.queue.is_empty and player.queue.mode == wavelink.QueueMode.normal:
            text_channel = getattr(player, "home", None)

            await asyncio.sleep(DELAY)

            if player.current is None and player.queue.is_empty:
                await player.disconnect()

                if text_channel is not None and isinstance(text_channel, discord.abc.Messageable):
                    embed = await CustomEmbed.create(
                        guild,
                        key="app.events.wavelink.idle_disconnect",
                        client=self.bot,
                    )
                    await text_channel.send(embed=embed)
            return

        if not player.queue.is_empty and not player.playing:
            next_track = player.queue.get()
            await player.play(next_track)
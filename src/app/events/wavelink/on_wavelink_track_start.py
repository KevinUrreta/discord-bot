import logging

import discord
import wavelink
from discord.ext import commands

from src.helpers import metadata
from src.helpers.embed import CustomEmbed
from src.helpers.formatting import format_duration
from src.infrastructure.database.repositories.guild_settings import GuildSettingsRepository

logger = logging.getLogger("discord")


class OnWavelinkTracksStart(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            return

        channel = getattr(player, "home", None)
        if not channel or not isinstance(channel, discord.abc.Messageable):
            return

        guild: discord.Guild | None = player.guild
        if not guild:
            return

        try:
            repo = GuildSettingsRepository(self.client.db)
            settings = await repo.read(guild.id)
            if settings and settings.volume is not None:
                await player.set_volume(settings.volume)
            autoplay_mode = settings.autoplay.lower() if settings and settings.autoplay else "disabled"
            if autoplay_mode == "enabled":
                player.autoplay = wavelink.AutoPlayMode.enabled
            elif autoplay_mode == "partial":
                player.autoplay = wavelink.AutoPlayMode.partial
            else:
                player.autoplay = wavelink.AutoPlayMode.disabled
        except Exception as e:
            logger.error(f"Error synchronizing settings: {e}")

        track: wavelink.Playable = payload.track
        data = await metadata.get_original_info(track.uri or "", track)

        track_extras = dict(track.extras)
        author_name = track_extras.get("author_name", self.client.user.display_name)
        author_avatar = track_extras.get("author_avatar")
        if author_avatar is None and self.client.user:
            author_avatar = self.client.user.display_avatar.url

        await channel.send(embed = await CustomEmbed.create(
            guild,
            key="app.commands.music.play.now_playing",
            client=self.client,
            thumbnail=data.get("thumbnail", None),
            url=track.uri or data.get("uri") or "",
            title=data.get("title", "Título desconocido"),
            duration=format_duration(track.length),
            views=data.get("views", "N/A"),
            queue=player.queue.count,
            user=author_name,
            footer_icon=author_avatar
        ))

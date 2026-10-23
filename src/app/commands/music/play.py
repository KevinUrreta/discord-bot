from typing import cast

import discord
import wavelink
from discord.ext import commands

from src.helpers import metadata
from src.helpers.embed import CustomEmbed
from src.helpers.formatting import format_duration


class Play(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx: commands.Context, *, query: str | None = None):
        if not ctx.guild:
            return
        if not query:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.play.missing_song",
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url if ctx.author.display_avatar else None
            ))
            return

        player: wavelink.Player = cast("wavelink.Player", ctx.voice_client)

        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            except AttributeError:
                await ctx.send(embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.play.voice_not_connected",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url
                ))
                return
            except discord.ClientException:
                await ctx.send(embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.play.unable_connect",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url
                ))
                return

        # Turn on AutoPlay to enabled mode.
        # enabled = AutoPlay will play songs for us and fetch recommendations...
        # partial = AutoPlay will play songs for us, but WILL NOT fetch recommendations...
        # disabled = AutoPlay will do nothing...
        player.autoplay = wavelink.AutoPlayMode.enabled

        # Lock the player to this channel...
        if not hasattr(player, "home"):
            setattr(player, "home", ctx.channel)
        elif getattr(player, "home") != ctx.channel:
            home_channel = getattr(player, "home")
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.play.already_playing",
                channel=home_channel.mention,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        # This will handle fetching Tracks and Playlists...
        # Seed the doc strings for more information on this method...
        # If spotify is enabled via LavaSrc, this will automatically fetch Spotify tracks if you pass a URL...
        # Defaults to YouTube for non URL based queries...
        if query.startswith("https://"):
            tracks: wavelink.Search = await wavelink.Playable.search(query)
        else:
            tracks: wavelink.Search = await wavelink.Playable.search(query, source="ytsearch")
        if not tracks:
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.play.no_song_found",
                member=ctx.author.mention,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
            return

        if isinstance(tracks, wavelink.Playlist):
            # tracks is a playlist...
            added: int = await player.queue.put_wait(tracks)
            await ctx.send(embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.play.playlist_added_to_queue",
                title=tracks.name,
                queue=added,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url
            ))
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            data: metadata.TrackMetadata = await metadata.get_original_info(track.uri or query, track)

            if player.playing:
                await ctx.send(embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.play.added_to_queue",
                    title=data.get("title", "Título desconocido"),
                    queue=player.queue.count,
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url
                ))
            else:
                await ctx.send(embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.play.now_playing",
                    thumbnail=data.get("thumbnail", ""),
                    title=data.get("title", "Título desconocido"),
                    duration=format_duration(track.length),
                    views=data.get("views", 0),
                    queue=player.queue.count,
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url
                ))

        if not player.playing:
            # Play now since we aren't playing anything...
            await player.play(player.queue.get(), volume=30)

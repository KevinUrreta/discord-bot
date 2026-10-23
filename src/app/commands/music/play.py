from typing import cast

import discord
import wavelink
from discord.ext import commands

from src.i18n.translate import i18n


class Play(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx: commands.Context, *, query: str):
        if not ctx.guild:
            return

        player: wavelink.Player = cast("wavelink.Player", ctx.voice_client)

        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            except AttributeError:
                await ctx.send(await i18n(ctx, "app.commands.music.play.not_connected"))
                return
            except discord.ClientException:
                await ctx.send(await i18n(ctx, "app.commands.music.play.unable_connect"))
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
            await ctx.send(await i18n(ctx, "app.commands.music.play.already_playing", channel=home_channel))
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
            await ctx.send(await i18n(ctx, "app.commands.music.play.not_found"))
            return

        if isinstance(tracks, wavelink.Playlist):
            # tracks is a playlist...
            added: int = await player.queue.put_wait(tracks)
            await ctx.send(await i18n(ctx, "app.commands.music.play.playlist_add", name=tracks.name, added=added))
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            await ctx.send(await i18n(ctx, "app.commands.music.play.queue_add", track=track))

        if not player.playing:
            # Play now since we aren't playing anything...
            await player.play(player.queue.get(), volume=30)

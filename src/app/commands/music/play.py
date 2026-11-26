import wavelink
from discord.ext import commands

from src.helpers import metadata
from src.helpers.embed import CustomEmbed


class Play(commands.Cog):
    """Componente que permite reproducir música en los canales de voz.

    Permite a los usuarios buscar y reproducir pistas de audio en el servidor.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *, query: str):
        """Busca y reproduce una canción o lista de reproducción.

        Soporta búsqueda por nombre, URL directa o playlists de YouTube.

        :param ctx: Contexto del comando de Discord.
        :param query: Búsqueda o URL de la canción a reproducir.
        """
        if ctx.voice_client is None:
            if not ctx.author.voice:
                await ctx.send(
                    embed=await CustomEmbed.create(
                        ctx,
                        key="app.commands.music.play.voice_not_connected",
                        user=ctx.author.display_name,
                        footer_icon=ctx.author.display_avatar.url,
                    )
                )
                return

            player: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            player = ctx.voice_client

        # Lock the player to this channel...
        if not hasattr(player, "home"):
            player.home = ctx.channel
        elif player.home != ctx.channel:
            home_channel = player.home
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.play.already_playing",
                    channel=home_channel.mention,
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return

        tracks = (
            await wavelink.Playable.search(query)
            if query.startswith("https://")
            else await wavelink.Playable.search(query, source="ytsearch")
        )

        if not tracks:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.play.no_song_found",
                    member=ctx.author.mention,
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return

        if isinstance(tracks, wavelink.Playlist):
            # tracks is a playlist...
            added: int = await player.queue.put_wait(tracks)
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.play.playlist_added_to_queue",
                    title=tracks.name,
                    queue=added,
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
        else:
            track: wavelink.Playable = tracks[0]
            track.extras = {
                "author_name": ctx.author.display_name,
                "author_avatar": str(ctx.author.display_avatar.url),
            }

            await player.queue.put_wait(track)
            data: metadata.TrackMetadata = await metadata.get_original_info(
                track.uri or query, track
            )

            if player.playing:
                await ctx.send(
                    embed=await CustomEmbed.create(
                        ctx,
                        key="app.commands.music.play.added_to_queue",
                        title=data.get("title", "Título desconocido"),
                        queue=player.queue.count,
                        user=ctx.author.display_name,
                        footer_icon=ctx.author.display_avatar.url,
                    )
                )

        if not player.playing:
            # Play now since we aren't playing anything...
            await player.play(player.queue.get())

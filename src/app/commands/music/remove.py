import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed


class Remove(commands.Cog):
    """Componente que permite eliminar una canción de la cola de reproducción.

    Permite a los usuarios remover una pista específica de la cola de música.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(name="remove")
    async def remove(self, ctx, position: int):
        """Elimina una canción específica de la cola de reproducción.

        Remueve la pista en la posición indicada sin afectar otras pistas.

        :param ctx: Contexto del comando de Discord.
        :param position: Posición de la canción en la cola (1-based).
        """
        if ctx.voice_client is None:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.remove.not_connected",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return
        player: wavelink.Player = ctx.voice_client
        if player.queue.is_empty:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.remove.queue_empty",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return

        playlist = list[wavelink.Playable](player.queue)
        if position < 1 or position > len(playlist):
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.remove.invalid_position",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return
        song = playlist[position - 1]
        player.queue.remove(song)

        await ctx.send(
            embed=await CustomEmbed.create(
                ctx,
                key="app.commands.music.remove.success",
                title=song.title,
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            )
        )

import wavelink
from discord.ext import commands

from src.helpers.embed import CustomEmbed


class Loop(commands.Cog):
    """Componente que gestiona el modo de bucle de la cola de reproducción.

    Permite a los usuarios alternar entre reproducción normal y repetida de la cola.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(name="loop")
    async def loop(self, ctx):
        """Alterna el modo de bucle de la cola.

        :param ctx: Contexto del comando de Discord.
        """
        if ctx.voice_client is None:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.loop.not_connected",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return
        player: wavelink.Player = ctx.voice_client

        if not player.current:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.loop.no_song_playing",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return
        player.queue.mode = (
            wavelink.QueueMode.loop
            if player.queue.mode != wavelink.QueueMode.loop
            else wavelink.QueueMode.normal
        )
        if player.queue.mode == wavelink.QueueMode.loop:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.loop.enabled",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
        else:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.music.loop.disabled",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )

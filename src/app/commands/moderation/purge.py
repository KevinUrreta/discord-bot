from discord.ext import commands

from src.helpers import permissions
from src.helpers.embed import CustomEmbed


class Purge(commands.Cog):
    """Componente que permite eliminar mensajes de un canal de texto en Discord.

    Permite a los moderadores purgar un número determinado de mensajes en el canal actual.

    :param client: Instancia del cliente principal del bot.
    """

    def __init__(self, client):
        self.client = client

    @permissions.has_manage_messages()
    @commands.command(name="purge")
    async def purge(self, ctx, amount: int):
        """Elimina mensajes en un canal de texto.

        :param ctx: Contexto del mensaje.
        :param amount: Número de mensajes que se eliminarán.
        """
        if amount < 1:
            await ctx.send(
                embed=await CustomEmbed.create(
                    ctx,
                    key="app.commands.moderation.purge.invalid_amount",
                    user=ctx.author.display_name,
                    footer_icon=ctx.author.display_avatar.url,
                )
            )
            return

        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(
            embed=await CustomEmbed.create(
                ctx,
                key="app.commands.moderation.purge.success",
                amount=len(deleted),
                user=ctx.author.display_name,
                footer_icon=ctx.author.display_avatar.url,
            ),
            delete_after=5,
        )

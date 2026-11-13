import discord
from discord.ext import commands

from src.core.exceptions import (
    ManageGuildRequired,
    ManageMessagesRequired,
)


def has_manage_messages():
    """Verificador de permisos para gestionar mensajes en un canal.

    :return: Decorador de comando que verifica permisos de manage_messages.
    """

    async def predicate(ctx) -> bool:
        if (
            not isinstance(ctx.author, discord.Member)
            or not ctx.author.guild_permissions.manage_messages
        ):
            raise ManageMessagesRequired()

        return True

    return commands.check(predicate)


def has_manage_guild():
    """Verificador de permisos para gestionar el servidor.

    :return: Decorador de comando que verifica permisos de manage_guild.
    """

    async def predicate(ctx) -> bool:
        if (
            not isinstance(ctx.author, discord.Member)
            or not ctx.author.guild_permissions.manage_guild
        ):
            raise ManageGuildRequired()

        return True

    return commands.check(predicate)

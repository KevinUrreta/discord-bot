import discord
from discord.ext import commands

from src.core.exceptions import (
    NotPlaying,
    SameVoiceChannelRequired,
    VoiceChannelRequired,
)


def is_in_voice_channel():
    """Verificador para comandos que requieren estar en canal de voz.

    :return: Decorador que verifica presencia en canal de voz.
    """

    async def predicate(ctx) -> bool:
        if (
            not isinstance(ctx.author, discord.Member)
            or not ctx.author.voice
            or not ctx.author.voice.channel
        ):
            raise VoiceChannelRequired()

        return True

    return commands.check(predicate)


def is_in_same_voice_channel():
    """Verificador para comandos que requieren estar en el mismo canal de voz.

    :return: Decorador que verifica coincidencia de canal de voz.
    """

    async def predicate(ctx) -> bool:
        if (
            not isinstance(ctx.author, discord.Member)
            or not ctx.author.voice
            or not ctx.author.voice.channel
        ):
            raise VoiceChannelRequired()

        if not ctx.voice_client or ctx.author.voice.channel != ctx.voice_client.channel:
            raise SameVoiceChannelRequired()

        return True

    return commands.check(predicate)


def is_playing():
    """Verificador para comandos que requieren que la música esté reproduciéndose.

    :return: Decorador que verifica estado de reproducción.
    """

    async def predicate(ctx) -> bool:
        if (
            not ctx.voice_client
            or not getattr(ctx.voice_client, "is_playing", lambda: False)()
        ):
            raise NotPlaying()

        return True

    return commands.check(predicate)

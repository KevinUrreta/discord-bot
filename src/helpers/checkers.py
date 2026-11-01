import discord
from discord.ext import commands
from src.core.exceptions import (
    VoiceChannelRequired,
    SameVoiceChannelRequired,
    NotPlaying,
)

def is_in_voice_channel():
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
    async def predicate(ctx) -> bool:
        if (
            not isinstance(ctx.author, discord.Member)
            or not ctx.author.voice
            or not ctx.author.voice.channel
        ):
            raise VoiceChannelRequired()

        if (
            not ctx.voice_client
            or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            raise SameVoiceChannelRequired()

        return True

    return commands.check(predicate)

def is_playing():
    async def predicate(ctx) -> bool:
        if (
            not ctx.voice_client
            or not getattr(ctx.voice_client, "is_playing", lambda: False)()
        ):
            raise NotPlaying()

        return True

    return commands.check(predicate)

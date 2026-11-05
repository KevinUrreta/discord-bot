from discord.ext import commands

from src.core.exceptions import (
    CheckFailure,
    ManageGuildRequired,
    ManageMessagesRequired,
    NotPlaying,
    SameVoiceChannelRequired,
    VoiceChannelRequired,
)


def test_custom_command_checks_are_check_failures() -> None:
    exceptions = (
        CheckFailure,
        ManageGuildRequired,
        ManageMessagesRequired,
        NotPlaying,
        SameVoiceChannelRequired,
        VoiceChannelRequired,
    )

    assert all(issubclass(exception, commands.CheckFailure) for exception in exceptions)

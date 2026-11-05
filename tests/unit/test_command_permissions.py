import asyncio
from types import SimpleNamespace
from unittest.mock import Mock

import discord
import pytest

from src.app.commands.info.prefix import Prefix
from src.app.commands.moderation.purge import Purge
from src.core.exceptions import ManageGuildRequired, ManageMessagesRequired


@pytest.mark.parametrize(
    ("command", "permission", "error"),
    [
        (Prefix.prefix, "manage_guild", ManageGuildRequired),
        (Purge.purge, "manage_messages", ManageMessagesRequired),
    ],
)
def test_restricted_command_check_rejects_missing_permission(
    command, permission: str, error: type[Exception]
) -> None:
    author = Mock(spec=discord.Member)
    author.guild_permissions = SimpleNamespace(**{permission: False})
    context = SimpleNamespace(author=author)
    check = command.checks[0]

    with pytest.raises(error):
        asyncio.run(check(context))


@pytest.mark.parametrize(
    ("command", "permission"),
    [
        (Prefix.prefix, "manage_guild"),
        (Purge.purge, "manage_messages"),
    ],
)
def test_restricted_command_check_accepts_granted_permission(
    command, permission: str
) -> None:
    author = Mock(spec=discord.Member)
    author.guild_permissions = SimpleNamespace(**{permission: True})
    context = SimpleNamespace(author=author)
    check = command.checks[0]

    assert asyncio.run(check(context)) is True

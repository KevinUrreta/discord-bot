import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import wavelink

from src.app.commands.moderation.purge import Purge
from src.app.commands.music.join import Join
from src.app.commands.music.stop import Stop
from src.helpers.embed import CustomEmbed


def make_context():
    user = SimpleNamespace(
        display_name="Test user",
        display_avatar=SimpleNamespace(url="https://example.test/avatar.png"),
        voice=None,
    )
    channel = SimpleNamespace(purge=AsyncMock())
    return SimpleNamespace(
        author=user,
        channel=channel,
        voice_client=None,
        send=AsyncMock(),
    )


async def make_embed(*args, **kwargs):
    return "test embed"


def test_purge_does_not_delete_messages_when_amount_is_zero(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    context = make_context()
    command = Purge(client=None)

    asyncio.run(Purge.purge.callback(command, context, 0))

    context.channel.purge.assert_not_awaited()
    context.send.assert_awaited_once_with(embed="test embed")


def test_purge_deletes_the_requested_number_of_messages(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    context = make_context()
    context.channel.purge.return_value = ["message 1", "message 2"]
    command = Purge(client=None)

    asyncio.run(Purge.purge.callback(command, context, 5))

    context.channel.purge.assert_awaited_once_with(limit=5)
    context.send.assert_awaited_once_with(
        embed="test embed",
        delete_after=5,
    )


def test_join_does_nothing_when_user_is_not_in_voice():
    context = make_context()
    command = Join(client=None)

    asyncio.run(Join.join.callback(command, context))

    context.send.assert_not_awaited()


def test_stop_clears_the_queue_and_stops_the_player(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    queue = SimpleNamespace(reset=Mock())
    player = SimpleNamespace(
        autoplay=None,
        current="current track",
        queue=queue,
        stop=AsyncMock(),
    )
    context = make_context()
    context.voice_client = player
    command = Stop(client=None)

    asyncio.run(Stop.stop.callback(command, context))

    assert player.autoplay is wavelink.AutoPlayMode.disabled
    assert player.stop_requested is True
    queue.reset.assert_called_once_with()
    player.stop.assert_awaited_once_with()
    context.send.assert_awaited_once_with(embed="test embed")

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import wavelink

from src.app.events.voice.on_voice_state_update import OnVoiceStateUpdate


def make_voice_state_update(members):
    channel = SimpleNamespace(members=members)
    player = SimpleNamespace(
        autoplay=wavelink.AutoPlayMode.enabled,
        channel=channel,
        disconnect=AsyncMock(),
    )
    guild = SimpleNamespace(voice_client=player)
    member = SimpleNamespace(guild=guild)
    before = SimpleNamespace(channel=channel)
    after = SimpleNamespace(channel=None)
    return member, before, after, player


def test_disconnects_and_disables_autoplay_when_channel_is_empty():
    bot_member = SimpleNamespace(bot=True)
    member, before, after, player = make_voice_state_update([bot_member])

    asyncio.run(OnVoiceStateUpdate(None).on_voice_state_update(member, before, after))

    assert player.autoplay is wavelink.AutoPlayMode.disabled
    player.disconnect.assert_awaited_once_with()


def test_keeps_playing_while_a_human_remains_in_channel():
    bot_member = SimpleNamespace(bot=True)
    human_member = SimpleNamespace(bot=False)
    member, before, after, player = make_voice_state_update([bot_member, human_member])

    asyncio.run(OnVoiceStateUpdate(None).on_voice_state_update(member, before, after))

    assert player.autoplay is wavelink.AutoPlayMode.enabled
    player.disconnect.assert_not_awaited()

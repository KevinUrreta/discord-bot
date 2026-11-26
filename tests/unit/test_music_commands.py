import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import wavelink

from src.app.commands.music.clear import Clear
from src.app.commands.music.leave import Leave
from src.app.commands.music.loop import Loop
from src.app.commands.music.now_playing import NowPlaying
from src.app.commands.music.pause import Pause
from src.app.commands.music.play import Play
from src.app.commands.music.queue import Queue
from src.app.commands.music.remove import Remove
from src.app.commands.music.resume import Resume
from src.app.commands.music.shuffle import Shuffle
from src.app.commands.music.skip import Skip
from src.helpers.embed import CustomEmbed


class FakeQueue:
    def __init__(self, tracks=None):
        self.tracks = tracks or []
        self.remove = Mock()

    @property
    def is_empty(self):
        return len(self.tracks) == 0

    @property
    def count(self):
        return len(self.tracks)

    def __iter__(self):
        return iter(self.tracks)


async def make_embed(*args, **kwargs):
    return "test embed"


def make_context(player=None):
    user = SimpleNamespace(
        display_name="Test user",
        display_avatar=SimpleNamespace(url="https://example.test/avatar.png"),
        mention="@test-user",
        voice=None,
    )
    channel = SimpleNamespace(mention="#music")
    return SimpleNamespace(
        author=user,
        channel=channel,
        guild=SimpleNamespace(id=123),
        voice_client=player,
        send=AsyncMock(),
    )


def test_clear_removes_tracks_from_queue(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    queue = SimpleNamespace(is_empty=False, clear=Mock())
    context = make_context(SimpleNamespace(queue=queue))

    asyncio.run(Clear.clear.callback(Clear(None), context))

    queue.clear.assert_called_once_with()
    context.send.assert_awaited_once_with(embed="test embed")


def test_remove_deletes_track_at_given_position(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    first_track = SimpleNamespace(title="First track")
    second_track = SimpleNamespace(title="Second track")
    queue = FakeQueue([first_track, second_track])
    player = SimpleNamespace(queue=queue)
    context = make_context(player)

    asyncio.run(Remove.remove.callback(Remove(None), context, 2))

    queue.remove.assert_called_once_with(second_track)
    context.send.assert_awaited_once_with(embed="test embed")


def test_remove_does_not_change_queue_for_invalid_position(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    queue = FakeQueue([SimpleNamespace(title="Only track")])
    context = make_context(SimpleNamespace(queue=queue))

    asyncio.run(Remove.remove.callback(Remove(None), context, 2))

    queue.remove.assert_not_called()
    context.send.assert_awaited_once_with(embed="test embed")


def test_shuffle_shuffles_queue_with_multiple_tracks(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    queue = SimpleNamespace(count=2, shuffle=Mock())
    context = make_context(SimpleNamespace(queue=queue))

    asyncio.run(Shuffle.shuffle.callback(Shuffle(None), context))

    queue.shuffle.assert_called_once_with()
    context.send.assert_awaited_once_with(embed="test embed")


def test_loop_turns_loop_mode_on(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    queue = SimpleNamespace(mode=wavelink.QueueMode.normal)
    player = SimpleNamespace(queue=queue, current="Current track")
    context = make_context(player)

    asyncio.run(Loop.loop.callback(Loop(None), context))

    assert queue.mode == wavelink.QueueMode.loop
    context.send.assert_awaited_once_with(embed="test embed")


def test_pause_pauses_current_track(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    player = SimpleNamespace(playing=True, pause=AsyncMock())
    context = make_context(player)

    asyncio.run(Pause.pause.callback(Pause(None), context))

    player.pause.assert_awaited_once_with(True)
    context.send.assert_awaited_once_with(embed="test embed")


def test_resume_resumes_paused_track(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    player = SimpleNamespace(paused=True, pause=AsyncMock())
    context = make_context(player)

    asyncio.run(Resume.resume.callback(Resume(None), context))

    player.pause.assert_awaited_once_with(False)
    context.send.assert_awaited_once_with(embed="test embed")


def test_skip_skips_current_track(monkeypatch):
    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    player = SimpleNamespace(current="Current track", skip=AsyncMock())
    context = make_context(player)

    asyncio.run(Skip.skip.callback(Skip(None), context))

    player.skip.assert_awaited_once_with(force=True)
    context.send.assert_awaited_once_with(embed="test embed")


def test_leave_disconnects_player(monkeypatch):
    embed_mock = AsyncMock(return_value="test embed")
    monkeypatch.setattr(CustomEmbed, "create", embed_mock)
    player = SimpleNamespace(disconnect=AsyncMock())
    context = make_context(player)

    asyncio.run(Leave.leave.callback(Leave(None), context))

    player.disconnect.assert_awaited_once_with()
    assert (
        embed_mock.await_args.kwargs["key"] == "app.commands.music.leave.disconnected"
    )
    context.send.assert_awaited_once_with(embed="test embed")


def test_leave_reports_when_not_connected(monkeypatch):
    embed_mock = AsyncMock(return_value="test embed")
    monkeypatch.setattr(CustomEmbed, "create", embed_mock)
    context = make_context()

    asyncio.run(Leave.leave.callback(Leave(None), context))

    embed_mock.assert_awaited_once()
    assert (
        embed_mock.await_args.kwargs["key"] == "app.commands.music.leave.not_connected"
    )
    context.send.assert_awaited_once_with(embed="test embed")


def test_queue_shows_track_titles(monkeypatch):
    from src.app.commands.music import queue as queue_module

    embed_mock = AsyncMock(return_value="test embed")
    monkeypatch.setattr(CustomEmbed, "create", embed_mock)
    monkeypatch.setattr(
        queue_module.metadata,
        "get_original_info",
        AsyncMock(return_value={"title": "Test song"}),
    )
    track = SimpleNamespace(uri="https://example.test/song")
    queue = FakeQueue([track])
    player = SimpleNamespace(queue=queue)
    context = make_context(player)

    asyncio.run(Queue.queue.callback(Queue(None), context))

    assert embed_mock.await_args.kwargs["queue"] == ("1. *Test song*")
    context.send.assert_awaited_once_with(embed="test embed")


def test_now_playing_shows_current_track(monkeypatch):
    from src.app.commands.music import now_playing as now_playing_module

    embed_mock = AsyncMock(return_value="test embed")
    monkeypatch.setattr(CustomEmbed, "create", embed_mock)
    monkeypatch.setattr(
        now_playing_module,
        "get_original_info",
        AsyncMock(return_value={"title": "Test song"}),
    )
    track = SimpleNamespace(uri="https://example.test/song", length=90_000)
    player = SimpleNamespace(current=track, queue=SimpleNamespace(count=0))
    context = make_context(player)
    command = NowPlaying(client=SimpleNamespace())

    asyncio.run(NowPlaying.nowplaying.callback(command, context))

    embed_arguments = embed_mock.await_args.kwargs
    assert embed_arguments["title"] == "Test song"
    assert embed_arguments["duration"] == "1:30"
    context.send.assert_awaited_once_with(embed="test embed")


def test_play_shows_message_when_user_is_not_in_voice(monkeypatch):
    from src.app.commands.music import play as play_module

    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    search = AsyncMock()
    monkeypatch.setattr(play_module.wavelink.Playable, "search", search)
    context = make_context()

    asyncio.run(Play(None).play.callback(Play(None), context, query="test song"))

    search.assert_not_awaited()
    context.send.assert_awaited_once_with(embed="test embed")


def test_play_shows_message_when_search_has_no_results(monkeypatch):
    from src.app.commands.music import play as play_module

    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    search = AsyncMock(return_value=[])
    monkeypatch.setattr(play_module.wavelink.Playable, "search", search)
    context = make_context(SimpleNamespace())

    asyncio.run(Play(None).play.callback(Play(None), context, query="unknown song"))

    search.assert_awaited_once_with("unknown song", source="ytsearch")
    context.send.assert_awaited_once_with(embed="test embed")


def test_play_adds_track_to_queue_and_starts_player(monkeypatch):
    from src.app.commands.music import play as play_module

    monkeypatch.setattr(CustomEmbed, "create", make_embed)
    track = SimpleNamespace(uri="https://example.test/song", extras=None)
    monkeypatch.setattr(
        play_module.wavelink.Playable,
        "search",
        AsyncMock(return_value=[track]),
    )
    monkeypatch.setattr(
        play_module.metadata,
        "get_original_info",
        AsyncMock(return_value={"title": "Test song"}),
    )
    queue = SimpleNamespace(
        put_wait=AsyncMock(),
        get=Mock(return_value=track),
    )
    player = SimpleNamespace(playing=False, queue=queue, play=AsyncMock())
    context = make_context(player)

    asyncio.run(Play(None).play.callback(Play(None), context, query="test song"))

    queue.put_wait.assert_awaited_once_with(track)
    player.play.assert_awaited_once_with(track)
    assert track.extras["author_name"] == "Test user"
    context.send.assert_not_awaited()


def test_play_adds_playlist_to_queue(monkeypatch):
    from src.app.commands.music import play as play_module

    class FakePlaylist:
        name = "Test playlist"

    queue = SimpleNamespace(
        put_wait=AsyncMock(return_value=3),
        get=Mock(return_value="first track"),
    )
    player = SimpleNamespace(
        queue=queue,
        playing=False,
        play=AsyncMock(),
    )
    context = make_context(player)
    playlist = FakePlaylist()
    monkeypatch.setattr(play_module.wavelink, "Playlist", FakePlaylist)
    monkeypatch.setattr(
        play_module.wavelink.Playable,
        "search",
        AsyncMock(return_value=playlist),
    )
    embed_mock = AsyncMock(return_value="test embed")
    monkeypatch.setattr(CustomEmbed, "create", embed_mock)

    asyncio.run(Play(None).play.callback(Play(None), context, query="playlist"))

    queue.put_wait.assert_awaited_once_with(playlist)
    embed_mock.assert_awaited_once()
    assert embed_mock.await_args.kwargs["title"] == "Test playlist"
    assert embed_mock.await_args.kwargs["queue"] == 3
    player.play.assert_awaited_once_with("first track")

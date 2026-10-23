import asyncio
from typing import TypedDict

import wavelink
import yt_dlp


class TrackMetadata(TypedDict):
    title: str
    views: int
    thumbnail: str


async def get_original_info(url: str, track: wavelink.Playable) -> TrackMetadata:
    def extract():
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
            try:
                return ydl.extract_info(url, download=False) or {}
            except Exception:
                return {}

    info = await asyncio.to_thread(extract)

    return {
        "title": info.get("title", "Título desconocido"),
        "views": info.get("view_count", 0),
        "thumbnail": info.get("thumbnail") or track.artwork or f"https://youtube.com{track.identifier}/hqdefault.jpg"
    }

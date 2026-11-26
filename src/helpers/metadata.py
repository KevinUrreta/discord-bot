import asyncio
from typing import TypedDict

import wavelink
import yt_dlp


class TrackMetadata(TypedDict):
    """Metadatos de una pista de música extraídos desde YouTube."""

    title: str
    views: int
    thumbnail: str


async def get_original_info(url: str, track: wavelink.Playable) -> TrackMetadata:
    """Obtiene información original de una pista de YouTube.

    Extrae metadatos usando yt_dlp en un hilo separado.

    :param url: URL de la pista a consultar.
    :param track: Objeto Playable de wavelink.
    :return: Diccionario con metadatos de la pista.
    """

    def extract():
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
            try:
                return ydl.extract_info(url, download=False) or {}
            except Exception:
                return {}

    info = await asyncio.to_thread(extract)

    title: str = info.get("title") or "Unknown Title"
    views: int = info.get("view_count") or 0
    thumbnail: str = (
        info.get("thumbnail") or track.artwork or "https://i.imgur.com/6X3Z1Qk.png"
    )

    return {"title": title, "views": views, "thumbnail": thumbnail}

from typing import Any, Union

import discord
from discord.ext import commands

from src.i18n.translate import i18n


class CustomEmbed:
    @staticmethod
    async def _format_value(value: Any, kwargs: dict) -> Any:
        if isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError:
                return value
        if isinstance(value, list):
            return [await CustomEmbed._format_value(item, kwargs) for item in value]
        if isinstance(value, dict):
            return {k: await CustomEmbed._format_value(v, kwargs) for k, v in value.items()}
        return value

    @classmethod
    async def create(
            cls,
            target: Union[commands.Context, discord.Guild, None],
            key: str,
            *,
            thumbnail: str | None = None,
            timestamp: bool = True,
            color: discord.Color = discord.Color.purple(),
            client: discord.Client | None = None,
            **kwargs,
    ) -> discord.Embed:

        raw_data = await i18n(target, key, client=client, **kwargs)

        if isinstance(raw_data, str) and raw_data == key:
            raise ValueError(f"Embed translation '{key}' does not exist.")

        if isinstance(raw_data, str):
            data = {"description": raw_data}
        else:
            data = await cls._format_value(raw_data, kwargs)

        if not isinstance(data, dict):
            raise ValueError(f"Embed translation '{key}' must be a dictionary or object structure.")

        embed = discord.Embed(
            title=data.get("title"),
            description=data.get("description"),
            color=color,
        )
        if timestamp:
            embed.timestamp = discord.utils.utcnow()
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        fields = data.get("fields")
        if fields and isinstance(fields, list):
            for field in fields:
                embed.add_field(
                    name=field.get("name", ""),
                    value=field.get("value", ""),
                    inline=field.get("inline", False),
                )

        footer_data = data.get("footer")
        if footer_data:
            if isinstance(footer_data, str):
                embed.set_footer(text=footer_data)
            elif isinstance(footer_data, dict):
                embed.set_footer(
                    text=footer_data.get("text"),
                    icon_url=footer_data.get("icon_url") or kwargs.get("footer_icon"),
                )

        return embed

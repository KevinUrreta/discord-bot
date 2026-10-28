import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

import discord
from discord.ext import commands

from src.infrastructure.database.repositories.guild_settings import GuildSettingsRepository


class Translator:
    def __init__(self) -> None:
        self.__locales_dir = Path(__file__).parent / "locales"
        self.__translations: Dict[str, Dict[str, Any]] = {}
        self.__default_lang = "en-US"
        self.__load_locales()
        self.__setup_normalization()

    def __load_locales(self) -> None:
        if not self.__locales_dir.exists():
            return

        for file_path in self.__locales_dir.glob("*.json"):
            lang_code = file_path.stem
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.__translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"Error loading language file {lang_code}: {e}")

    def __setup_normalization(self) -> None:
        self.supported = list[str] (self.__translations.keys())
        self.mapping = {}
        for code in self.supported:
            canonical = code
            self.mapping[canonical] = canonical
            self.mapping[canonical.lower()] = canonical
            self.mapping[canonical.upper()] = canonical

            short_code = code.split("-")[0].split("_")[0]
            self.mapping[short_code] = canonical
            self.mapping[short_code.lower()] = canonical
            self.mapping[short_code.upper()] = canonical

    def normalize(self, lang_input: str) -> Optional[str]:
        if not lang_input:
            return None
        return self.mapping.get(lang_input.strip())

    def get_supported_languages(self) -> list[str]:
        return self.supported

    async def __get_guild_language(self, client, guild_id: Optional[int]) -> str:
        if client is None or guild_id is None:
            return self.__default_lang

        repo = GuildSettingsRepository(client.db)
        settings = await repo.read(guild_id)
        if settings and settings.language:
            normalized = self.normalize(settings.language)
            if normalized:
                return normalized

        return self.__default_lang

    @staticmethod
    def __traverse(data: Any, keys: list) -> Any:
        for k in keys:
            if isinstance(data, dict) and k in data:
                data = data[k]
            else:
                return None
        return data

    async def translate(self, target: Union[commands.Context, discord.Guild, None], key: str, *,
                        client: discord.Client | None = None, **kwargs: Any) -> Union[
        str, Dict[str, Any], list]:
        if isinstance(target, commands.Context):
            guild = target.guild
            client = target.bot
        elif isinstance(target, discord.Guild):
            guild = target
        else:
            guild = None

        lang = await self.__get_guild_language(client, guild.id if guild else None)

        keys = key.split(".")

        result = self.__traverse(self.__translations.get(lang), keys)

        if result is None:
            result = self.__traverse(self.__translations.get(self.__default_lang), keys)

        if result is None:
            return key

        if isinstance(result, str):
            if kwargs:
                try:
                    return result.format(**kwargs)
                except KeyError:
                    return result
            return result

        return result


translator = Translator()
i18n = translator.translate

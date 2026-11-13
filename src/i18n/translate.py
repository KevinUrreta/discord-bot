import json
from pathlib import Path
from typing import Any

import discord
from discord.ext import commands

from src.infrastructure.database.repositories.guild_settings import (
    GuildSettingsRepository,
)


class Translator:
    """Gestor de traducciones internacionalizadas para el bot.

    Carga archivos JSON de traducciones y proporciona métodos para normalizar
    códigos de idioma y obtener traducciones contextualizadas por servidor.
    """

    def __init__(self) -> None:
        """Inicializa el traductor y carga los archivos de idioma disponibles."""
        self.__locales_dir = Path(__file__).parent / "locales"
        self.__translations: dict[str, dict[str, Any]] = {}
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
        self.supported = list[str](self.__translations.keys())
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

    def normalize(self, lang_input: str) -> str | None:
        """Normaliza un código de idioma a su forma canónica.

        :param lang_input: Código de idioma a normalizar.
        :return: Código canónico o None si no es soportado.
        """
        if not lang_input:
            return None
        return self.mapping.get(lang_input.strip())

    def get_supported_languages(self) -> list[str]:
        """Devuelve la lista de idiomas soportados.

        :return: Lista de códigos de idioma disponibles.
        """
        return self.supported

    async def __get_guild_language(self, client, guild_id: int | None) -> str:
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

    async def translate(
        self,
        target: commands.Context | discord.Guild | None,
        key: str,
        *,
        client: discord.Client | None = None,
        **kwargs: Any,
    ) -> str | dict[str, Any] | list:
        """Traduce una clave al idioma del servidor.

        :param target: Contexto del comando o Guild de Discord.
        :param key: Clave de la cadena a traducir.
        :param client: Instancia del cliente de Discord.
        :param kwargs: Argumentos para formatear la cadena.
        :return: Cadena traducida, diccionario o lista.
        """
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

import importlib
import logging
from collections import defaultdict
from pathlib import Path
from typing import TypedDict

from discord.ext import commands

logger = logging.getLogger("discord")


class LoadStats(TypedDict):
    total: int
    loaded: int
    failed: list[tuple[str, str, Exception]]


async def load_module(client) -> None:
    """Carga dinámicamente los módulos de comandos, eventos y tareas.

    Recorre las carpetas de la aplicación y carga todos los Cogs definidos
    en los módulos Python encontrados.

    :param client: Instancia del cliente de Discord para registrar los Cogs.
    """
    base_path = Path(__file__).resolve().parent.parent
    categories: dict[tuple[str, str], LoadStats] = defaultdict(
        lambda: {"total": 0, "loaded": 0, "failed": []}
    )

    for cog_type in ("commands", "events", "tasks"):
        cog_path = base_path / "app" / cog_type

        if not cog_path.exists():
            continue

        for file in cog_path.rglob("*.py"):
            if file.name.startswith("_"):
                continue

            category = file.parent.name
            key: tuple[str, str] = (cog_type, category)
            categories[key]["total"] += 1

            relative_path = file.relative_to(base_path.parent)
            module_path = ".".join(relative_path.with_suffix("").parts)

            try:
                module = importlib.import_module(module_path)

                for attribute in vars(module).values():
                    if (
                        isinstance(attribute, type)
                        and issubclass(attribute, commands.Cog)
                        and attribute is not commands.Cog
                        and attribute.__module__ == module.__name__
                    ):
                        cog = attribute(client)
                        await client.add_cog(cog)
                        categories[key]["loaded"] += 1

            except Exception as error:
                categories[key]["failed"].append(
                    (file.name, type(error).__name__, error)
                )

    for (cog_type, category), data in categories.items():
        label = cog_type.capitalize()

        if data["failed"]:
            for filename, error_type, exc in data["failed"]:
                logger.error(
                    f"{label} | {category} | Error loading {filename} | {error_type}: {exc}"
                )
            continue

        if data["loaded"] > 0:
            logger.info(
                f"{label} | {category} | successfully loaded ({data['loaded']})"
            )

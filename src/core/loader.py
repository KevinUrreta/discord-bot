import importlib
from pathlib import Path
import logging
from discord.ext import commands

logger = logging.getLogger("discord")


async def load_module(client):
    base_path = Path(__file__).resolve().parent.parent
    for cog_type in ("commands", "events", "tasks"):
        cog_path = base_path / "app" / cog_type

        if not cog_path.exists():
            continue

        for file in cog_path.rglob("*.py"):
            if file.name.startswith("_"):
                continue

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
                        logger.info(f"Loaded successful: {module_path} -> {attribute.__name__}")

            except Exception as e:
                logger.error(f"Error loading module {module_path}: {e}")
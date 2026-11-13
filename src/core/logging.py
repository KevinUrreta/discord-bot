import logging
from pathlib import Path

from src.core.config import Settings

settings = Settings()

formatter = logging.Formatter(
    fmt="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

path = Path(settings.log_file)
path.parent.mkdir(parents=True, exist_ok=True)

cli = logging.StreamHandler()
cli.setFormatter(formatter)

file = logging.FileHandler(path, encoding="utf-8")
file.setLevel(logging.INFO)
file.setFormatter(formatter)

root = logging.getLogger()
root.setLevel(logging.INFO)

if not root.handlers:
    root.addHandler(cli)
    root.addHandler(file)

discord = logging.getLogger("discord")
discord.setLevel(logging.INFO)
discord.propagate = True

logger = logging.getLogger()

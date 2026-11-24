import asyncio

import src.core.logging  # noqa
from src.app.client import Client
from src.core.config import Settings


async def main() -> None:
    # noinspection argument-list
    settings = Settings()

    async with Client(settings) as client:
        await client.start(settings.discord_token.get_secret_value())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

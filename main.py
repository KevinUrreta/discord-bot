import asyncio

import src.core.logging  # noqa
from src.app.client import Client
from src.core.config import Settings


async def main():
    settings = Settings()
    async with Client() as client:
        try:
            await client.start(settings.discord_token.get_secret_value())
        finally:
            await client.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
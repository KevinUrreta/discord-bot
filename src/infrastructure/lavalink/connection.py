import wavelink

from src.core.config import Settings
from src.core.logging import logger


class Lavalink:

    @staticmethod
    async def connect_lavalink(bot):
        if wavelink.Pool.nodes:
            return

        settings = Settings()

        try:
            await wavelink.Pool.connect(
                nodes=[
                    wavelink.Node(
                        identifier="main",
                        uri=f"http://{settings.lavalink_host}:{settings.lavalink_port}",
                        password=settings.lavalink_password,
                    )
                ],
                client=bot,
            )
            logger.info("Lavalink node connected successfully.")
        except Exception as e:
            logger.error(f"Error on connecting Lavalink: {e}")

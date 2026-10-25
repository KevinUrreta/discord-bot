import logging

import wavelink

logger = logging.getLogger("discord")


class Lavalink:

    @staticmethod
    async def connect_lavalink(client) -> None:
        if wavelink.Pool.nodes:
            return

        settings = client.settings

        try:
            # noinspection HttpUrlsUsage
            await wavelink.Pool.connect(
                nodes=[
                    wavelink.Node(
                        identifier="main",
                        uri=f"http://{settings.lavalink_host}:{settings.lavalink_port}",
                        password=settings.lavalink_password.get_secret_value(),
                    )
                ],
                client=client,
            )
            logger.info("Lavalink node connected successfully.")
        except Exception:
            logger.exception("Error connecting to Lavalink.")
            raise

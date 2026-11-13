import logging

import wavelink

logger = logging.getLogger("discord")


class Lavalink:
    """Gestiona la conexión con el nodo Lavalink para reproducción de música.

    Proporciona métodos para conectar el bot con el servidor Lavalink.
    """

    @staticmethod
    async def connect_lavalink(client) -> None:
        """Conecta el bot al servidor Lavalink.

        Establece la conexión con el pool de nodos Lavalink usando la configuración.

        :param client: Instancia del cliente principal del bot.
        """
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

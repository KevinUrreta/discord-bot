from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from sqlalchemy import URL, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])
P = ParamSpec("P")
R = TypeVar("R")


def with_session(func: Callable[..., Awaitable[R]]) -> Callable[..., Awaitable[R]]:
    """Decorador que gestiona sesiones de base de datos automáticamente.

    Proporciona una sesión de AsyncSession al método decorado y
    maneja commit/rollback automáticamente.

    :param func: Función a decorar que requiere sesión de base de datos.
    :return: Función decorada con gestión de sesión.
    """

    @wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> R:
        async with self._db.get_session() as session:
            return await func(self, *args, **kwargs, session=session)

    return wrapper


class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos ORM de la base de datos."""


class Database:
    """Gestor de conexión a la base de datos PostgreSQL asíncrona.

    Proporciona métodos para crear tablas, gestionar sesiones y cerrar conexiones.

    :param url: URL de conexión a la base de datos.
    """

    def __init__(self, url: str | URL) -> None:
        """Inicializa la conexión a la base de datos.

        :param url: URL de conexión a la base de datos.
        """
        self.engine = create_async_engine(url, pool_pre_ping=True)
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """Proporciona una sesión de base de datos con manejo automático de transacciones.

        :return: Context manager con sesión async.
        """
        async with self.session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def _ensure_postgres_columns(self) -> None:
        required_columns = {
            "guild_settings": [
                ("autoplay", "VARCHAR(20) NOT NULL DEFAULT 'disabled'"),
            ]
        }

        async with self.engine.begin() as connection:
            for table_name, columns in required_columns.items():
                for column_name, column_ddl in columns:
                    exists = await connection.execute(
                        text(
                            """
                            SELECT EXISTS (
                                SELECT 1
                                FROM information_schema.columns
                                WHERE table_schema = 'public'
                                  AND table_name = :table_name
                                  AND column_name = :column_name
                            )
                            """
                        ),
                        {"table_name": table_name, "column_name": column_name},
                    )
                    if not exists.scalar():
                        await connection.execute(
                            text(
                                f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {column_ddl}'
                            )
                        )

    async def create_tables(self):
        """Crea las tablas necesarias en la base de datos.

        Incluye migración de columnas faltantes para compatibilidad.
        """
        try:
            async with self.engine.begin() as connection:
                await connection.run_sync(
                    lambda sync_conn: Base.metadata.create_all(bind=sync_conn)
                )

            await self._ensure_postgres_columns()
        except Exception:
            raise

    async def close(self) -> None:
        """Cierra la conexión a la base de datos.

        Libera recursos del engine de SQLAlchemy.
        """
        await self.engine.dispose()

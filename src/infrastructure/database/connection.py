from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])
P = ParamSpec("P")
R = TypeVar("R")


def with_session(func: Callable[..., Awaitable[R]]) -> Callable[..., Awaitable[R]]:
    @wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> R:
        async with self._db.get_session() as session:
            return await func(self, *args, **kwargs, session=session)

    return wrapper


class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos ORM de la base de datos."""
    pass


class Database:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url, pool_pre_ping=True)
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def create_tables(self):
        try:
            from src.infrastructure.database.models import GuildModel, GuildSettingsModel, UserModel, MemberModel
            async with self.engine.begin() as connection:
                await connection.run_sync(lambda sync_conn: Base.metadata.create_all(bind=sync_conn))
        except Exception:
            raise

    async def close(self) -> None:
        await self.engine.dispose()

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect

from src.infrastructure.database.connection import Base, Database, with_session

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], database: Database) -> None:
        self.model = model
        self._db = database

    @with_session
    async def list_all(self, session: AsyncSession) -> list[ModelType]:
        result = await session.scalars(select(self.model))
        return list(result.all())

    @with_session
    async def create(self, session: AsyncSession, **data: Any) -> ModelType:
        obj = self.model(**data)
        session.add(obj)
        await session.flush()
        return obj

    @with_session
    async def read(self, *keys: object, session: AsyncSession) -> ModelType | None:
        key = keys[0] if len(keys) == 1 else tuple(keys)
        return await session.get(self.model, key)

    @with_session
    async def update(self, *keys: object, session: AsyncSession, **data: Any) -> ModelType | None:
        obj = await self.read_in_session(session, *keys)
        if obj is None:
            return None
        mapper = inspect(self.model)
        columns = {attr.key for attr in mapper.column_attrs}
        primary = {column.key for column in mapper.primary_key}
        if set(data) - columns or set(data) & primary:
            raise ValueError("Campo desconocido o clave primaria no modificable")
        for field, value in data.items():
            setattr(obj, field, value)
        await session.flush()
        return obj

    async def read_in_session(self, session: AsyncSession, *keys: object) -> ModelType | None:
        key = keys[0] if len(keys) == 1 else tuple(keys)
        return await session.get(self.model, key)

    @with_session
    async def delete(self, *keys: object, session: AsyncSession) -> bool:
        obj = await self.read_in_session(session, *keys)
        if obj is None:
            return False
        await session.delete(obj)
        return True

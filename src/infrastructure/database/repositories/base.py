from typing import Generic, Type, TypeVar, Optional, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.base import Base
from src.infrastructure.database.connection import Database

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], database: Database):
        self.model = model
        self.database = database

    async def get_by_id(self, *primary_keys) -> Optional[ModelType]:
        async with self.database.get_session() as session:
            return await session.get(self.model, primary_keys)

    async def delete_by_id(self, *primary_keys) -> bool:
        async with self.database.get_session() as session:
            obj = await session.get(self.model, primary_keys)
            if obj is None:
                return False
            await session.delete(obj)
            return True
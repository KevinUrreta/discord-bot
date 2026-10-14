from sqlalchemy import select
from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.user import UserModel
from src.infrastructure.database.repositories.base import BaseRepository

class UserRepository(BaseRepository[UserModel]):
    def __init__(self, database: Database) -> None:
        super().__init__(UserModel, database)

    async def create_or_update(self, user_id: int, username: str) -> UserModel:
        async with self.database.get_session() as session:
            user = await session.get(UserModel, user_id)
            if user is not None:
                if user.username != username:
                    user.username = username
                    await session.refresh(user)
                return user

            user = UserModel(id=user_id, username=username)
            session.add(user)
            await session.flush()
            await session.refresh(user)
            return user

    async def get(self, user_id: int) -> UserModel | None:
        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> bool:
        return await self.delete_by_id(user_id)
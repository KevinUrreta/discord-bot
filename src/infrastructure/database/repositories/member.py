from datetime import datetime, timezone
from sqlalchemy import select
from src.infrastructure.database.connection import Database
from src.infrastructure.database.models.member import MemberModel
from src.infrastructure.database.repositories.base import BaseRepository


class MemberRepository(BaseRepository[MemberModel]):
    def __init__(self, database: Database) -> None:
        super().__init__(MemberModel, database)

    async def create_or_update(
            self,
            user_id: int,
            guild_id: int,
            nickname: str | None = None,
            joined_guild_at: datetime | None = None,
    ) -> MemberModel:
        async with self.database.get_session() as session:
            member = await self.get(user_id, guild_id)

            if joined_guild_at is not None and joined_guild_at.tzinfo is None:
                joined_guild_at = joined_guild_at.replace(tzinfo=timezone.utc)

            if member is not None:
                updated = False

                if member.nickname != nickname:
                    member.nickname = nickname
                    updated = True

                if joined_guild_at is not None and member.joined_guild_at != joined_guild_at:
                    member.joined_guild_at = joined_guild_at
                    updated = True

                if updated:
                    await session.flush()
                    await session.refresh(member)

                return member

            member = MemberModel(
                user_id=user_id,
                guild_id=guild_id,
                nickname=nickname,
                joined_guild_at=joined_guild_at or datetime.now(timezone.utc),
            )

            session.add(member)
            await session.flush()
            await session.refresh(member)

            return member

    async def get(self, user_id: int, guild_id: int) -> MemberModel | None:
        return await self.get_by_id(user_id, guild_id)

    async def delete(self, user_id: int, guild_id: int) -> bool:  # type: ignore[override]
        return await self.delete_by_id(user_id, guild_id)

    async def delete_by_guild(self, guild_id: int) -> int:
        async with self.database.get_session() as session:
            result = await session.execute(
                select(MemberModel).where(MemberModel.guild_id == guild_id)
            )
            members = list(result.scalars().all())

            if not members:
                return 0

            for member in members:
                await session.delete(member)
            await session.flush()

            return len(members)
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.infrastructure.database.models.member import MemberModel
    from src.infrastructure.database.models.guild_settings import GuildSettingsModel


class GuildModel(Base):
    __tablename__ = "guilds"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc)
    )

    settings: Mapped[Optional["GuildSettingsModel"]] = relationship(
        back_populates="guild",
        cascade="all, delete-orphan",
        uselist=False
    )

    members: Mapped[List["MemberModel"]] = relationship(
        back_populates="guild",
        cascade="all, delete-orphan"
    )

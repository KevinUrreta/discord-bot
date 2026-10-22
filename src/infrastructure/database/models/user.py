from datetime import datetime, timezone
from typing import List, TYPE_CHECKING

from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.connection import Base

if TYPE_CHECKING:
    from src.infrastructure.database.models.member import MemberModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    memberships: Mapped[List["MemberModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

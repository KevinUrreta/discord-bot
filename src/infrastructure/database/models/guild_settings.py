from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.infrastructure.database.models.guild import GuildModel


class GuildSettingsModel(Base):
    __tablename__ = "guild_settings"

    guild_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("guilds.id", ondelete="CASCADE"),
        primary_key=True
    )

    prefix: Mapped[str] = mapped_column(String(10), default="!", nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    volume: Mapped[int] = mapped_column(default=100, nullable=False)

    guild: Mapped["GuildModel"] = relationship(back_populates="settings")

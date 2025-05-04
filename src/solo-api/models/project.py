from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date
from typing import Optional

from datetime import datetime, timezone, date
from .base import EntityModel


class Project(EntityModel):
    __tablename__ = "project"

    start_date: Mapped[date] = mapped_column(
        Date,
        default=lambda: datetime.now(timezone.utc).date(),
        index=True,
    )
    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        default=None,
        index=True,
    )
    header_url: Mapped[Optional[str]] = mapped_column(String, default=None)
    cover_url: Mapped[Optional[str]] = mapped_column(String, default=None)

    def __repr__(self) -> str:
        return f"<Project(id='{self.id}', name='{self.name}')>"

from sqlalchemy.orm import Mapped, WriteOnlyMapped, mapped_column, relationship
from sqlalchemy import Text, Date
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
    header_url: Mapped[Optional[str]] = mapped_column(Text, default=None)
    cover_url: Mapped[Optional[str]] = mapped_column(Text, default=None)

    # One-to-many with attachment
    attachments: WriteOnlyMapped["Attachment"] = relationship(  # noqa:F821
        "Attachment",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Attachment.created_at.desc()",
    )

    # Many-to-many with tag
    tags: WriteOnlyMapped["ProjectTagAssociation"] = relationship(  # noqa:F821
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProjectTagAssociation.created_at.desc()",
    )

    def __repr__(self) -> str:
        return f"<Project(id='{self.id}', name='{self.name}')>"

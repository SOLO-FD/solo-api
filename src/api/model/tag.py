from sqlalchemy.orm import Mapped, WriteOnlyMapped, mapped_column, relationship
from sqlalchemy import String

from .base import EntityModel


class Tag(EntityModel):
    __tablename__ = "tag"

    color: Mapped[str] = mapped_column(String(7))

    # Many-to-many with tag
    projects: WriteOnlyMapped["ProjectTagAssociation"] = relationship(  # noqa:F821
        back_populates="tag",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ProjectTagAssociation.created_at.desc()",
    )

    def __repr__(self) -> str:
        return f"<Tag(id='{self.id}', name='{self.name}')>"

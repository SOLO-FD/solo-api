from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime, timezone
from src.api.database import Base


class ProjectTagAssociation(Base):
    __tablename__ = "project_tag_association"

    # ID
    project_id: Mapped[str] = mapped_column(ForeignKey("project.id"), primary_key=True)
    tag_id: Mapped[str] = mapped_column(ForeignKey("tag.id"), primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    # Relationship
    project: Mapped["Project"] = relationship(  # noqa: F821
        "Project",
        back_populates="tags",
        lazy="raise",
    )

    tag: Mapped["Tag"] = relationship(  # noqa: F821
        "Tag",
        back_populates="projects",
        lazy="raise",
    )

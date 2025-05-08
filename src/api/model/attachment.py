from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger, ForeignKey, Text
from ..enums import FileType

from .base import BaseModel


class Attachment(BaseModel):
    __tablename__ = "attachment"

    filename: Mapped[str] = mapped_column(String(128), index=True)
    file_type: Mapped[FileType] = mapped_column(String(10), index=True)
    url: Mapped[str] = mapped_column(Text)
    size: Mapped[int] = mapped_column(BigInteger)

    # By SHA256
    checksum: Mapped[str] = mapped_column(String(64), unique=True)

    # Many-to-one with project
    project_id: Mapped[str] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE")
    )
    project: Mapped["Project"] = relationship(  # noqa:F821
        "Project",
        back_populates="attachments",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return f"<Attachment(id='{self.id}', filename='{self.filename}')>"

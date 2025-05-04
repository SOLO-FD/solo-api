from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from typing import Optional
from nanoid import generate
from datetime import datetime, timezone

from ..database import Base


# All tables should have id and created_at
class BaseModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(default=lambda: generate(size=13), primary_key=True)

    # Use lambda to create a callable
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )


# All entities should have name, description, and updated_at
class EntityModel(BaseModel):
    __abstract__ = True

    name: Mapped[str] = mapped_column(String(128), index=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)

from sqlmodel import Field, SQLModel
from nanoid import generate
from datetime import datetime, timezone


# All tables should have id and created_at
class BaseModel(SQLModel):
    id: str = Field(default_factory=lambda: generate(size=13), primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )


# All entities should have name, description, and updated_at
class EntityModel(BaseModel):
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )

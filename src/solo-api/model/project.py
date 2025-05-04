from sqlmodel import Field
from datetime import datetime, timezone, date
from base import EntityModel


class Project(EntityModel, table=True):
    start_date: date = Field(
        default_factory=lambda: datetime.now(timezone.utc).date(), index=True
    )
    end_date: date | None = Field(default=None, index=True)
    header_img: str | None = Field(default=None)
    cover_img: str | None = Field(default=None)

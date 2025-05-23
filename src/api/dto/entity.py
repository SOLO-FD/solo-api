from typing import Optional
from datetime import datetime
from .base import (
    BaseDTO,
    BaseCreateDTOMixin,
    BaseUpdateDTOMixin,
    BasePublicDTOMixin,
)


class EntityDTO(BaseDTO):
    description: Optional[str] = None


class EntityCreateDTOMixin(BaseCreateDTOMixin):
    name: str


class EntityUpdateDTOMixin(BaseUpdateDTOMixin):
    name: Optional[str] = None


class EntityPublicDTOMixin(BasePublicDTOMixin):
    name: str
    updated_at: datetime

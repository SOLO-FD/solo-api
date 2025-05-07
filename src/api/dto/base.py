from pydantic import BaseModel
from datetime import datetime


class BaseDTO(BaseModel):
    pass


class BaseCreateDTOMixin:
    pass


class BaseUpdateDTOMixin:
    pass


class BasePublicDTOMixin:
    id: str
    created_at: datetime

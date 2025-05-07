from .base import BaseDTO
from .tag import TagPublicDTO
from datetime import datetime


class ProjectTagCreateDTO(BaseDTO):
    tag_id: str


class ProjectTagPublicDTO(BaseDTO):
    created_at: datetime
    tag: TagPublicDTO

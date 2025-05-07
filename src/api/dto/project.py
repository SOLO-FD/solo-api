from .entity import (
    EntityDTO,
    EntityCreateDTOMixin,
    EntityUpdateDTOMixin,
    EntityPublicDTOMixin,
)
from .attachment import (
    AttachmentCreateDTO,
    AttachmentPublicDTO,
)
from typing import Optional
from datetime import date


class ProjectBaseDTO(EntityDTO):
    end_date: Optional[date] = None
    header_url: Optional[str] = None
    cover_url: Optional[str] = None


class ProjectCreateDTO(ProjectBaseDTO, EntityCreateDTOMixin):
    start_date: date
    attachments: list[AttachmentCreateDTO] = []


class ProjectUpdateDTO(ProjectBaseDTO, EntityUpdateDTOMixin):
    start_date: Optional[str] = None
    attachments: Optional[list[AttachmentCreateDTO]] = None


class ProjectPublicDTO(ProjectBaseDTO, EntityPublicDTOMixin):
    start_date: date
    attachments: list[AttachmentPublicDTO] = []

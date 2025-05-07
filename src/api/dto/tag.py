from .entity import (
    EntityDTO,
    EntityCreateDTOMixin,
    EntityUpdateDTOMixin,
    EntityPublicDTOMixin,
)
from typing import Optional


class TagBaseDTO(EntityDTO):
    pass


class TagCreateDTO(TagBaseDTO, EntityCreateDTOMixin):
    color: str


class TagUpdateDTO(TagBaseDTO, EntityUpdateDTOMixin):
    color: Optional[str] = None


class TagPublicDTO(TagBaseDTO, EntityPublicDTOMixin):
    color: str

from .base import (
    BaseDTO,
    BaseCreateDTOMixin,
    BasePublicDTOMixin,
)
from api.enums import FileType


class AttachmentDTO(BaseDTO):
    filename: str
    file_type: FileType
    url: str
    size: int
    checksum: str


class AttachmentCreateDTO(AttachmentDTO, BaseCreateDTOMixin):
    pass


class AttachmentPublicDTO(AttachmentDTO, BasePublicDTOMixin):
    pass

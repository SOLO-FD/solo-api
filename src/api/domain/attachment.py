from dataclasses import dataclass
from .base import BaseDomain
from ..enums import FileType


@dataclass(kw_only=True)
class AttachmentDomain(BaseDomain):
    filename: str
    file_type: FileType
    url: str
    size: int
    checksum: str

    def __repr__(self) -> str:
        return f"<AttachmentDomain(id='{self.id}', filename='{self.filename}')>"

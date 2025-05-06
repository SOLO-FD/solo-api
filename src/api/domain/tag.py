from dataclasses import dataclass
from .base import EntityDomain


@dataclass(kw_only=True, repr=False)
class TagDomain(EntityDomain):
    color: str

    def __repr__(self) -> str:
        return f"<TagDomain(id='{self.id}', name='{self.name}')>"

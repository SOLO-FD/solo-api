from dataclasses import dataclass
from .base import EntityDomain


@dataclass(kw_only=True)
class TagDomain(EntityDomain):
    color: str

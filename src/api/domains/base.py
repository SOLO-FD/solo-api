from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from nanoid import generate


@dataclass(kw_only=True)
class BaseDomain:
    id: str = field(default_factory=lambda: generate(size=13))
    created_at: Optional[datetime] = None


@dataclass(kw_only=True)
class EntityDomain(BaseDomain):
    name: str
    owner_id: str
    updated_at: Optional[datetime] = None
    description: Optional[str] = None

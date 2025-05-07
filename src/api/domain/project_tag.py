from dataclasses import dataclass
from datetime import datetime
from .tag import TagDomain


@dataclass(kw_only=True, repr=False)
class ProjectTagDomain:
    created_at: datetime
    tag: TagDomain

    def __repr__(self) -> str:
        return f"<ProjectTagDomain(tag_id='{self.tag.id}', created_at='{self.created_at}')>"

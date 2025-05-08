from .base import BaseDBService
from api.dto.tag import TagCreateDTO, TagUpdateDTO
from api.domain import TagDomain
from api.repo import TagRepo


class TagService(BaseDBService):
    def __init__(self, session):
        self._repo = TagRepo(session)

    async def create(self, owner_id: str, tag: TagCreateDTO) -> TagDomain:
        # Rebuild tag domain
        tag_domain = TagDomain(owner_id=owner_id, **tag.model_dump())

        return await self._repo.create(tag_domain)

    async def update(self, owner_id: str, tag_id: str, tag: TagUpdateDTO) -> TagDomain:
        # Get tag by id
        tag_from_repo = await self.get_by_id(owner_id, tag_id)

        # Update tag
        for key, updated_value in tag.model_dump().items():
            if updated_value is not None:
                setattr(tag_from_repo, key, updated_value)

        return await self._repo.update(tag_from_repo)

    async def get_by_id(self, owner_id: str, tag_id: str) -> TagDomain:
        tag_return = await self._repo.get_by_id(tag_id)
        if tag_return.owner_id != owner_id:
            raise ValueError(f"Tag with ID {tag_id} not existed")

        return tag_return

    async def list_by_owner_id(self, owner_id: str) -> list[TagDomain]:
        return await self._repo.list_by_owner_id(owner_id)

    async def delete_by_id(self, owner_id: str, tag_id: str) -> None:
        # Check if the given account owned the resource
        await self.get_by_id(owner_id, tag_id)

        return await self._repo.delete_by_id(tag_id)

    # === Project related service ===

from .base import BaseDBService
from api.dto.project_tag import ProjectTagCreateDTO
from api.domain import ProjectDomain, ProjectTagDomain
from api.repo import ProjectTagRepo, ProjectRepo, TagRepo


class ProjectTagService(BaseDBService):
    def __init__(self, session):
        self._session = session
        self._repo = ProjectTagRepo(session)

    async def add_tag_by_id(
        self, owner_id: str, project_id: str, tag_dto: ProjectTagCreateDTO
    ) -> list[ProjectTagDomain]:
        # Get tag_id from dto
        tag_id = tag_dto.tag_id

        # Check ownership
        await self._check_project_ownership(owner_id, project_id)
        await self._check_tag_ownership(owner_id, tag_id)

        # Add tag to project
        await self._repo.add_tag_by_id(project_id, tag_id)

        # Return updated set of tags
        return await self.list_by_project_id(owner_id, project_id)

    async def list_by_tag_id(self, owner_id: str, tag_id: str) -> list[ProjectDomain]:
        # Check ownership
        await self._check_tag_ownership(owner_id, tag_id)

        return await self._repo.list_by_tag_id(tag_id)

    async def list_by_project_id(
        self, owner_id: str, project_id: str
    ) -> list[ProjectTagDomain]:
        # Check ownership
        await self._check_project_ownership(owner_id, project_id)

        return await self._repo.list_by_project_id(project_id)

    async def remove_tag_by_id(
        self, owner_id: str, project_id: str, tag_id: str
    ) -> list[ProjectTagDomain]:
        # Check ownership
        await self._check_project_ownership(owner_id, project_id)
        await self._check_tag_ownership(owner_id, tag_id)

        await self._repo.remove_tag_by_id(project_id, tag_id)

        # Return updated set of tags
        return await self.list_by_project_id(owner_id, project_id)

    # === Private Methods Following ===
    async def _check_ownership(self, owner_id: str, entity_id: str, repo: type) -> None:
        entity = await repo(self._session).get_by_id(entity_id)

        # Check ownership
        if entity is None or entity.owner_id != owner_id:
            raise ValueError(
                f"{repo.__name__.replace('Repo', '')} with ID {entity.id} not existed."
            )

    async def _check_project_ownership(self, owner_id: str, project_id: str) -> None:
        return await self._check_ownership(owner_id, project_id, ProjectRepo)

    async def _check_tag_ownership(self, owner_id: str, tag_id: str) -> None:
        return await self._check_ownership(owner_id, tag_id, TagRepo)

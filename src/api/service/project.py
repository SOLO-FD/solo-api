from .base import BaseDBService
from src.api.dto.project import ProjectCreateDTO, ProjectUpdateDTO
from src.api.domain import ProjectDomain
from src.api.repo import ProjectRepo


class ProjectService(BaseDBService):
    def __init__(self, session):
        self._repo = ProjectRepo(session)

    async def create(self, project: ProjectCreateDTO) -> ProjectDomain:
        # Dump project
        project_dict = project.model_dump(exclude={"attachments"})

        # Rebuild project domain
        project_domain = ProjectDomain(**project_dict)

        # Add attachments
        project_domain.add_attachments(
            [attachment.model_dump() for attachment in project.attachments]
        )

        return await self._repo.create(project_domain)

    async def update(self, project_id: str, project: ProjectUpdateDTO) -> ProjectDomain:
        # Get project by id
        project_from_repo = await self._repo.get_by_id(project_id)

        # Get updated project params
        updated_param = project.model_dump(exclude={"attachments"})

        # Update project
        for key, updated_value in updated_param.items():
            if updated_value is not None:
                setattr(project_from_repo, key, updated_value)

        # Update attachment
        if project.attachments is not None:
            project_from_repo.add_attachments(
                [attachment.model_dump() for attachment in project.attachments]
            )

        return await self._repo.update(project_from_repo)

    async def get_by_id(self, project_id: str) -> ProjectDomain:
        pass

    async def list_by_owner_id(self, owner_id: str) -> list[ProjectDomain]:
        pass

    async def delete_by_id(self, project_id: str) -> None:
        pass

    async def list_by_tag_id(self, tag_id: str) -> list[ProjectDomain]:
        pass

    async def add_tag_by_id(self, project_id: str, tag_id: str) -> ProjectDomain:
        pass

    async def remove_tag_by_id(self, project_id: str, tag_id: str) -> ProjectDomain:
        pass

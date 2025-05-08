from .base import BaseDBService
from src.api.dto.project import ProjectCreateDTO, ProjectUpdateDTO
from src.api.domain import ProjectDomain
from src.api.repo import ProjectRepo


class ProjectService(BaseDBService):
    def __init__(self, session):
        self._repo = ProjectRepo(session)

    async def create(self, owner_id: str, project: ProjectCreateDTO) -> ProjectDomain:
        # Dump project
        project_dict = project.model_dump(exclude={"attachments"})

        # Rebuild project domain
        project_domain = ProjectDomain(owner_id=owner_id, **project_dict)

        # Add attachments
        project_domain.add_attachments(
            [attachment.model_dump() for attachment in project.attachments]
        )

        return await self._repo.create(project_domain)

    async def update(
        self, owner_id: str, project_id: str, project: ProjectUpdateDTO
    ) -> ProjectDomain:
        # Get project by id
        project_from_repo = await self.get_by_id(owner_id, project_id)

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

    async def get_by_id(self, owner_id: str, project_id: str) -> ProjectDomain:
        project_return = await self._repo.get_by_id(project_id)
        if project_return.owner_id != owner_id:
            raise ValueError(f"Project with ID {project_id} not existed")

        return project_return

    async def list_by_owner_id(self, owner_id: str) -> list[ProjectDomain]:
        return await self._repo.list_by_owner_id(owner_id)

    async def delete_by_id(self, owner_id: str, project_id: str) -> None:
        # Check if the given account owned the resource
        await self.get_by_id(owner_id, project_id)

        return await self._repo.delete_by_id(project_id)

    #  === Attachment-related Service ===
    async def remove_attachment_by_id(
        self, owner_id: str, project_id: str, attachment_id: str
    ) -> None:
        # Check if the given account owned the resource
        project_domain = await self.get_by_id(owner_id, project_id)

        # Remove attachments, return the refresh projects
        project_domain.remove_attachment_by_id(attachment_id)

        # Update project state
        await self._repo.update(project_domain)

        return project_domain

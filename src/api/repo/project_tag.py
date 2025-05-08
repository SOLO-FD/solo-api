from sqlalchemy import select
from .base import BaseSQLAlchemyRepo
from api.domain import ProjectDomain, ProjectTagDomain
from api.model import ProjectTagAssociation
from api.repo import ProjectRepo, TagRepo


class ProjectTagRepo(BaseSQLAlchemyRepo):
    async def add_tag_by_id(self, project_id: str, tag_id: str) -> None:
        # Check if tag existed
        tag_repo = TagRepo(self._session)
        await tag_repo.get_by_id(tag_id)

        # Create Association
        assoc = ProjectTagAssociation(project_id=project_id, tag_id=tag_id)

        self._session.add(assoc)
        await self._session.commit()

    async def list_by_tag_id(self, tag_id: str) -> list[ProjectDomain]:
        # Get assoc based on tag_id
        results = await self._session.scalars(
            select(ProjectTagAssociation).filter_by(tag_id=tag_id)
        )
        assocs = results.all()

        # Get project IDs
        selected_proj_ids = [assoc.project_id for assoc in assocs]

        # Get projects domain
        project_repo = ProjectRepo(self._session)
        project_domains = await project_repo.get_by_ids(selected_proj_ids)

        return project_domains

    async def list_by_project_id(self, project_id: str) -> list[ProjectTagDomain]:
        # Get assoc based on project_id
        results = await self._session.scalars(
            select(ProjectTagAssociation).filter_by(project_id=project_id)
        )
        assocs = results.all()

        # Get tag IDs
        assoc_dict = {assoc.tag_id: assoc for assoc in assocs}

        # Get tags domain
        tag_repo = TagRepo(self._session)
        tag_domains = await tag_repo.get_by_ids(list(assoc_dict.keys()))

        # Create dict for assoc based on ID
        project_tag_list = []
        for tag in tag_domains:
            assoc = assoc_dict[tag.id]
            project_tag_list.append(
                ProjectTagDomain(
                    created_at=assoc.created_at,
                    tag=tag,
                )
            )

        return project_tag_list

    async def remove_tag_by_id(self, project_id: str, tag_id: str) -> None:
        # Get assoc
        assoc = await self._session.get(
            ProjectTagAssociation,
            {"project_id": project_id, "tag_id": tag_id},
            populate_existing=True,
        )
        if assoc is None:
            raise ValueError(
                f"ProjectTagAssociation with Project ID {project_id} and Tag ID {tag_id} not existed."
            )

        await self._session.delete(assoc)
        await self._session.commit()

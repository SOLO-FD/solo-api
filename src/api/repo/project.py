from sqlalchemy import select, delete
from dataclasses import asdict
from .base import EntitySQLAlchemyRepo
from src.api.domain import ProjectDomain
from src.api.model import Project, Attachment, Tag, ProjectTagAssociation


class ProjectRepo(EntitySQLAlchemyRepo):
    async def create(self, project: ProjectDomain) -> ProjectDomain:
        drop_keys = {"_attachments"}

        # Create project, excluded drop_keys like children domain
        project_orm = self._domain_to_orm_mapper(project, Project, drop_keys)

        # Add attachments
        project_orm.attachments.add_all(
            [
                self._domain_to_orm_mapper(attachment, Attachment)
                for attachment in project.attachments
            ]
        )

        # Add and commit orm
        self._session.add(project_orm)
        commited_orm = await self._commit_domain_change(project_orm)

        return await self._orm_to_domain(commited_orm)

    async def get_by_id(self, project_id: str) -> ProjectDomain:
        # Get project orm by id
        proj_orm = await self._get_proj_from_db(project_id)

        # Build project domain from orm
        return await self._orm_to_domain(proj_orm)

    async def get_by_ids(self, project_ids: list) -> ProjectDomain:
        # Get project orm by ids
        proj_results = await self._session.scalars(
            select(Project).where(Project.id.in_(project_ids))
        )
        orms = proj_results.all()

        # Build project domain from orm
        return [await self._orm_to_domain(proj_orm) for proj_orm in orms]

    async def list_by_owner_id(self, owner_id: str) -> list[ProjectDomain]:
        # query for selecting given orm
        statement = select(Project).filter_by(owner_id=owner_id)

        # list of orm objects
        results = await self._session.scalars(statement)
        orms = results.all()

        return [await self._orm_to_domain(proj_orm) for proj_orm in orms]

    async def update(self, project: ProjectDomain) -> ProjectDomain:
        # Define allow fields
        drop_keys = {"id", "created_at", "updated_at", "owner_id", "_attachments"}
        allowed_fields = asdict(project).keys() - drop_keys

        # Get proj
        proj_orm = await self._get_proj_from_db(project.id)

        # Update proj
        for field in allowed_fields:
            setattr(proj_orm, field, getattr(project, field))

        # Update attachment
        await self._update_attachments(proj_orm, project)

        # Saved update
        commited_orm = await self._commit_domain_change(proj_orm)

        return await self._orm_to_domain(commited_orm)

    async def delete_by_id(self, project_id: str) -> None:
        # Get obj from db first
        proj_orm = await self._get_proj_from_db(project_id)
        await self._session.delete(proj_orm)

    #  === Tag-related ===
    async def add_tag_by_id(self, project_id: str, tag_id: str) -> None:
        # Check if tag existed
        if await self._session.get(Tag, tag_id, populate_existing=True) is None:
            raise ValueError(f"Tag with ID {tag_id} not existed.")

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

        # Get projects
        proj_results = await self._session.scalars(
            select(Project).where(Project.id.in_(selected_proj_ids))
        )
        orms = proj_results.all()

        return [await self._orm_to_domain(proj_orm) for proj_orm in orms]

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

    # === Private Methods ===

    async def _get_proj_from_db(self, project_id) -> Project:
        proj_orm = await self._session.get(Project, project_id, populate_existing=True)

        if proj_orm is None:
            raise ValueError(f"Project with ID {project_id} not existed")

        return proj_orm

    async def _update_attachments(
        self, prev_proj_orm: Project, update_proj_domain: ProjectDomain
    ):
        # Since run query before commit changed, use no_autoflush ensure commit together later
        with self._session.no_autoflush:
            # Clear existing attachments
            await self._session.execute(
                delete(Attachment).where(Attachment.project_id == prev_proj_orm.id)
            )

        # Create all attachments from update_proj_domain
        prev_proj_orm.attachments.add_all(
            [
                self._domain_to_orm_mapper(attachment, Attachment)
                for attachment in update_proj_domain.attachments
            ]
        )

    async def _orm_to_domain(self, proj_orm: Project) -> ProjectDomain:
        # Get proj domain
        proj = self._orm_to_domain_mapper(proj_orm, Project, ProjectDomain)

        # Add attachments
        results = await self._session.scalars(proj_orm.attachments.select())
        attachments = results.all()

        for attachment_orm in attachments:
            dict_orm = self._orm_to_dict_mapper(attachment_orm, Attachment)
            # Add to project
            proj.add_attachment(**dict_orm)

        return proj

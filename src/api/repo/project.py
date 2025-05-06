from sqlalchemy import select, delete
from dataclasses import asdict
from .base import BaseSQLALchemyRepo
from src.api.domain import ProjectDomain
from src.api.model import Project, Attachment


class ProjectRepo(BaseSQLALchemyRepo):
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
        proj_orm = await self._session.get(Project, project_id)

        # Build project domain from orm
        return await self._orm_to_domain(proj_orm)

    async def list_owned(self, account_id: str) -> list[ProjectDomain]:
        # query for selecting given orm
        statement = select(Project).filter_by(owner_id=account_id)

        # list of orm objects
        results = await self._session.scalars(statement)
        orms = results.all()

        return [await self._orm_to_domain(proj_orm) for proj_orm in orms]

    async def update(self, project: ProjectDomain) -> ProjectDomain:
        # Define allow fields
        drop_keys = {"id", "created_at", "updated_at", "owner_id", "_attachments"}
        allowed_fields = asdict(project).keys() - drop_keys

        # Get proj
        proj_orm = await self._session.get(Project, project.id)

        # Update proj
        for field in allowed_fields:
            setattr(proj_orm, field, getattr(project, field))

        # Update attachment
        await self._update_attachments(proj_orm, project)

        # Saved update
        commited_orm = await self._commit_domain_change(proj_orm)

        return await self._orm_to_domain(commited_orm)

    async def delete_by_id(self, project_id: str):
        pass

    # === Private Methods ===

    async def _update_attachments(
        self, prev_proj_orm: Project, update_proj_domain: ProjectDomain
    ):
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

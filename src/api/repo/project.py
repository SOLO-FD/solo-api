from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect
from dataclasses import asdict

from .base import BaseSQLALchemyRepo
from src.api.domain import ProjectDomain
from src.api.model import Project, Attachment


class ProjectRepo(BaseSQLALchemyRepo):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, project: ProjectDomain):
        drop_keys = {"_attachments"}

        # Create project, excluded drop_keys like children domain
        proj_dict = {
            key: value for key, value in asdict(project).items() if key not in drop_keys
        }
        project_orm = Project(
            **proj_dict,
        )

        # Add attachments
        project_orm.attachments.add_all(
            [Attachment(**asdict(attachment)) for attachment in project.attachments]
        )

        self._session.add(project_orm)
        await self._session.commit()
        await self._session.refresh(project_orm)

        return await self._orm_to_domain(project_orm)

    async def update(self, **kwargs):
        pass

    async def get_by_id(self, project_id: str):
        pass

    async def list(
        self,
    ):
        pass

    async def delete_by_id(self, project_id: str):
        pass

    async def _orm_to_domain(self, proj_orm: Project) -> ProjectDomain:
        drop_keys_proj = {}
        drop_keys_attachment = {}

        # Get proj domain
        proj = self._orm_to_domain_mapper(
            proj_orm, Project, ProjectDomain, drop_keys_proj
        )

        # Add attachments
        results = await self._session.scalars(proj_orm.attachments.select())
        attachments = results.all()

        for attachment_orm in attachments:
            mapper = inspect(Attachment)
            fields = [
                col.key for col in mapper.columns if col.key not in drop_keys_attachment
            ]

            # Get dict
            dict_orm = {
                k: v for k, v in inspect(attachment_orm).dict.items() if k in fields
            }
            # Add to project
            proj.add_attachment(**dict_orm)

        return proj

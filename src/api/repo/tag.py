from sqlalchemy import select
from dataclasses import asdict
from .base import BaseSQLALchemyRepo
from src.api.domain import TagDomain
from src.api.model import Tag, ProjectTagAssociation


class TagRepo(BaseSQLALchemyRepo):
    async def create(self, tag: TagDomain) -> TagDomain:
        drop_keys = {}

        # Create tag, excluded drop_keys like children domain
        tag_orm = self._domain_to_orm_mapper(tag, Tag, drop_keys)

        # Add and commit orm
        self._session.add(tag_orm)
        commited_orm = await self._commit_domain_change(tag_orm)

        return await self._orm_to_domain(commited_orm)

    async def get_by_id(self, tag_id: str) -> TagDomain:
        # Get tag orm by id
        tag_orm = await self._get_tag_from_db(tag_id)

        # Build tag domain from orm
        return await self._orm_to_domain(tag_orm)

    async def list_by_owner_id(self, account_id: str) -> list[TagDomain]:
        # query for selecting given orm
        statement = select(Tag).filter_by(owner_id=account_id)

        # list of orm objects
        results = await self._session.scalars(statement)
        orms = results.all()

        return [await self._orm_to_domain(tag_orm) for tag_orm in orms]

    async def list_by_project_id(self, project_id: str) -> list[TagDomain]:
        # Get assoc based on project_id
        results = await self._session.scalars(
            select(ProjectTagAssociation).filter_by(project_id=project_id)
        )

        assocs = results.all()

        # Get tag IDs
        selected_tag_ids = [assoc.tag_id for assoc in assocs]

        # Get tag
        tag_results = await self._session.scalars(
            select(Tag).where(Tag.id.in_(selected_tag_ids))
        )
        orms = tag_results.all()

        return [await self._orm_to_domain(tag_orm) for tag_orm in orms]

    async def update(self, tag: TagDomain) -> TagDomain:
        # Define allow fields
        drop_keys = {"id", "created_at", "updated_at", "owner_id"}
        allowed_fields = asdict(tag).keys() - drop_keys

        # Get tag
        tag_orm = await self._get_tag_from_db(tag.id)

        # Update tag
        for field in allowed_fields:
            setattr(tag_orm, field, getattr(tag, field))

        # Saved update
        commited_orm = await self._commit_domain_change(tag_orm)

        return await self._orm_to_domain(commited_orm)

    async def delete_by_id(self, tag_id: str):
        # Get obj from db first
        tag_orm = await self._get_tag_from_db(tag_id)
        await self._session.delete(tag_orm)

    # === Private Methods ===

    async def _get_tag_from_db(self, tag_id) -> Tag:
        tag_orm = await self._session.get(Tag, tag_id, populate_existing=True)

        if tag_orm is None:
            raise ValueError(f"Tag with ID {tag_id} not existed")

        return tag_orm

    async def _orm_to_domain(self, tag_orm: Tag) -> TagDomain:
        # Get tag domain
        tag = self._orm_to_domain_mapper(tag_orm, Tag, TagDomain)
        return tag

from abc import ABC, abstractmethod
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import asdict
from typing import Optional

from src.api.domain import BaseDomain
from src.api.model import BaseModel


class BaseSQLALchemyRepo(ABC):
    def __init__(self, session: AsyncSession):
        self._session = session

    @abstractmethod
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def list_by_owner_id(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, *args, **kwargs):
        raise NotImplementedError

    # === Private Helper Methods ===

    def _domain_to_orm_mapper(
        self, domain: BaseDomain, orm_cls: type, drop_keys: Optional[set] = None
    ) -> BaseModel:
        if drop_keys is None:
            drop_keys = set()
        # Create domain dict, excluded drop_keys
        domain_dict = {
            key: value for key, value in asdict(domain).items() if key not in drop_keys
        }
        return orm_cls(
            **domain_dict,
        )

    def _orm_to_domain_mapper(
        self,
        orm: BaseModel,
        orm_cls: type,
        domain_cls: type,
        drop_keys: Optional[set] = None,
    ) -> BaseDomain:
        # Create domain from dict of orm
        dict_orm = self._orm_to_dict_mapper(orm, orm_cls, drop_keys)
        return domain_cls(**dict_orm)

    def _orm_to_dict_mapper(
        self, orm: BaseModel, orm_cls: type, drop_keys: Optional[set] = None
    ) -> BaseDomain:
        if drop_keys is None:
            drop_keys = set()

        # Get all cols except drop_keys
        mapper = inspect(orm_cls)
        fields = [col.key for col in mapper.columns if col.key not in drop_keys]

        # Map orm to domain
        return {k: v for k, v in inspect(orm).dict.items() if k in fields}

    async def _commit_domain_change(self, orm: BaseModel) -> BaseModel:
        await self._session.commit()
        await self._session.refresh(orm)

        return orm

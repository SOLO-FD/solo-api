from abc import ABC, abstractmethod
from sqlalchemy import inspect

from src.api.domain import BaseDomain
from src.api.model import BaseModel


class BaseSQLALchemyRepo(ABC):
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
    async def list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, *args, **kwargs):
        raise NotImplementedError

    def _orm_to_domain_mapper(
        self, orm: BaseModel, orm_cls: type, domain_cls: type, drop_keys: set
    ) -> BaseDomain:
        # Get all cols except drop_keys
        mapper = inspect(orm_cls)
        fields = [col.key for col in mapper.columns if col.key not in drop_keys]

        # Map orm to domain
        dict_orm = {k: v for k, v in inspect(orm).dict.items() if k in fields}
        return domain_cls(**dict_orm)

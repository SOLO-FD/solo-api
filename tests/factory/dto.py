from dataclasses import asdict

from tests.factory.domains import (
    BaseDomainFactory,
)

from src.api.dto import (
    BaseDTO,
)


def new_dto_from_domain_factory(
    domain_factory: BaseDomainFactory, dto: BaseDTO, **kwargs
) -> BaseDTO:
    domain = domain_factory(**kwargs)
    return dto(**asdict(domain))

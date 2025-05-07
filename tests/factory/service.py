from src.api.service import ProjectService, TagService
from src.api.dto import (
    ProjectCreateDTO,
    AttachmentCreateDTO,
    TagCreateDTO,
)
from src.api.domain import ProjectDomain, TagDomain
from src.api.utils import generate_id
from tests.factory.domains import (
    ProjectDomainFactory,
    AttachmentDomainFactory,
    TagDomainFactory,
)
from tests.factory.dto import new_dto_from_domain_factory


async def create_project_by_service(
    session, attachment_num=3, owner_id=None, **kwargs
) -> ProjectDomain:
    project_dto = new_dto_from_domain_factory(
        ProjectDomainFactory,
        ProjectCreateDTO,
        **kwargs,
    )

    for _ in range(attachment_num):
        attachment_dto = new_dto_from_domain_factory(
            AttachmentDomainFactory,
            AttachmentCreateDTO,
        )
        project_dto.attachments.append(attachment_dto)

    service = ProjectService(session)
    if owner_id is None:
        owner_id = generate_id()

    return await service.create(owner_id, project_dto)


async def create_tag_by_service(session, owner_id=None, **kwargs) -> TagDomain:
    # Arrange: Create tag create DTO
    tag_dto = new_dto_from_domain_factory(
        TagDomainFactory,
        TagCreateDTO,
    )

    # Act: Create tag by service
    service = TagService(session)
    if owner_id is None:
        owner_id = generate_id()

    return await service.create(owner_id, tag_dto)

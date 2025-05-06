import pytest
from dataclasses import asdict
from src.api.repo import (
    ProjectRepo,
    TagRepo,
)
from tests.factory.domains import (
    ProjectDomainFactory,
    AttachmentDomainFactory,
    TagDomainFactory,
)


@pytest.fixture(name="default_project", scope="function")
async def _create_default_project_from_repo(session):
    repo = ProjectRepo(session)

    proj = ProjectDomainFactory()
    attachment = AttachmentDomainFactory()

    proj.add_attachment(**asdict(attachment))
    proj_from_repo = await repo.create(proj)

    return proj_from_repo


@pytest.fixture(name="default_tag", scope="function")
async def _create_default_tag_from_repo(session):
    repo = TagRepo(session)
    tag = TagDomainFactory()
    tag_from_repo = await repo.create(tag)

    return tag_from_repo

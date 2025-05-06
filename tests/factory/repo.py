from src.api.repo import (
    ProjectRepo,
    TagRepo,
)

from tests.factory.domains import (
    ProjectDomainFactory,
    TagDomainFactory,
)


# _create_project_from_repo
async def create_project(repo: ProjectRepo, **kwargs):
    proj = ProjectDomainFactory(**kwargs)
    proj_from_repo = await repo.create(proj)

    return proj_from_repo


async def create_tag(repo: TagRepo, **kwargs):
    tag = TagDomainFactory(**kwargs)
    tag_from_repo = await repo.create(tag)

    return tag_from_repo

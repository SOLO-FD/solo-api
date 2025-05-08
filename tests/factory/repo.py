from dataclasses import asdict

from api.repo import (
    ProjectRepo,
    TagRepo,
)

from tests.factory.domains import (
    ProjectDomainFactory,
    TagDomainFactory,
    AttachmentDomainFactory,
)


async def create_project(repo: ProjectRepo, **kwargs):
    proj = ProjectDomainFactory(**kwargs)
    proj_from_repo = await repo.create(proj)

    return proj_from_repo


async def create_project_with_attachments(repo: ProjectRepo, **kwargs):
    proj = ProjectDomainFactory(**kwargs)

    NEW_ATTCHMENTS = 7
    new_attachments = []
    for _ in range(NEW_ATTCHMENTS):
        attachment = AttachmentDomainFactory()
        new_attachments.append(asdict(attachment))

    proj.add_attachments(new_attachments)

    return await repo.create(proj)


async def create_tag(repo: TagRepo, **kwargs):
    tag = TagDomainFactory(**kwargs)
    tag_from_repo = await repo.create(tag)

    return tag_from_repo

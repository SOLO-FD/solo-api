import pytest
from tests.factory.repo import (
    create_project_with_attachments,
    create_tag,
)
from src.api.repo import ProjectRepo, TagRepo, ProjectTagRepo


@pytest.fixture(scope="function")
def default_header(default_account_id):
    return {
        "Framedesk-Account-ID": default_account_id,
    }


@pytest.fixture(scope="function")
async def default_project(session, default_account_id):
    return await create_project_with_attachments(
        ProjectRepo(session), owner_id=default_account_id
    )


@pytest.fixture(scope="function")
async def default_tag(session, default_account_id):
    return await create_tag(TagRepo(session), owner_id=default_account_id)


@pytest.fixture(scope="function")
async def default_tag_add_to_project(session, default_tag, default_project):
    await ProjectTagRepo(session).add_tag_by_id(default_project.id, default_tag.id)

    return await TagRepo(session).get_by_id(default_tag.id)

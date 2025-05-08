import pytest
from tests.factory.service import create_project_by_service, create_tag_by_service


@pytest.fixture(name="new_project", scope="function")
async def new_project(session, default_account_id):
    yield await create_project_by_service(session, owner_id=default_account_id)


@pytest.fixture(name="new_tag", scope="function")
async def new_tag(session, default_account_id):
    yield await create_tag_by_service(session, owner_id=default_account_id)

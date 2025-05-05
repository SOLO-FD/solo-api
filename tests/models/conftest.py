import pytest
from tests.factories.models import ProjectFactory


@pytest.fixture(scope="function")
async def default_project(session):
    project = ProjectFactory()

    session.add(project)
    await session.commit()
    await session.refresh(project)

    yield project

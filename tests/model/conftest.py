import pytest
from tests.factory.models import (
    ProjectFactory,
    AttachmentFactory,
    TagFactory,
)


@pytest.fixture(scope="function")
async def default_project(session):
    project = ProjectFactory()

    session.add(project)
    await session.commit()
    await session.refresh(project)

    yield project


@pytest.fixture(scope="function")
async def default_attachment(session):
    attachment = AttachmentFactory()

    session.add(attachment)
    await session.commit()
    await session.refresh(attachment)

    yield attachment


@pytest.fixture(scope="function")
async def default_tag(session):
    tag = TagFactory()

    session.add(tag)
    await session.commit()
    await session.refresh(tag)

    yield tag

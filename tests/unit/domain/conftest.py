import pytest
from tests.factory.domains import ProjectDomainFactory


@pytest.fixture(scope="function")
def default_project():
    project = ProjectDomainFactory()

    yield project

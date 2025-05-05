import pytest
from tests.factories.domains import ProjectDomainFactory


@pytest.fixture(scope="function")
def default_project():
    project = ProjectDomainFactory()

    yield project

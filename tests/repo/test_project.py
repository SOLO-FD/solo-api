import pytest
from dataclasses import asdict

from src.api.repo import ProjectRepo
from tests.factory.domains import ProjectDomainFactory, AttachmentDomainFactory


class TestProjectModelCase:
    @pytest.fixture(name="repo", scope="function")
    def _create_repo(self, session):
        return ProjectRepo(session)

    async def test_project_model_create_by_repo(self, repo):
        # Arrange: Create Project Domain
        proj = ProjectDomainFactory()

        # Arrange: Add attachment
        attachment = AttachmentDomainFactory()
        proj.add_attachment(**asdict(attachment))

        # Arrange: Setup the repo
        proj_from_repo = await repo.create(proj)

        # Assert: Check if the proj as expected
        assert proj_from_repo.id == proj.id
        assert proj_from_repo.get_attachment_by_id(attachment.id) is not None

import pytest
from dataclasses import asdict

from src.api.domain import ProjectDomain, AttachmentDomain
from src.api.model import Attachment
from src.api.repo import ProjectRepo
from tests.factory.domains import ProjectDomainFactory, AttachmentDomainFactory


class TestProjectModelCase:
    @pytest.fixture(name="repo", scope="function")
    def _create_repo(self, session):
        return ProjectRepo(session)

    @pytest.fixture(name="default_proj", scope="function")
    async def _create_default_project_from_repo(self, repo):
        proj = ProjectDomainFactory()
        attachment = AttachmentDomainFactory()

        proj.add_attachment(**asdict(attachment))
        proj_from_repo = await repo.create(proj)

        return proj_from_repo

    async def _create_project_from_repo(self, repo, **kwargs):
        proj = ProjectDomainFactory(**kwargs)
        proj_from_repo = await repo.create(proj)

        return proj_from_repo

    def _create_new_attachment(self, **kwargs) -> AttachmentDomain:
        return AttachmentDomainFactory(**kwargs)

    def _add_attachment_to_proj(
        self, proj: ProjectDomain, attachment: AttachmentDomain
    ):
        proj.add_attachment(**asdict(attachment))

    async def test_project_model_create_by_repo(self, repo):
        # Arrange: Create Project Domain
        proj = ProjectDomainFactory()

        # Arrange: Add attachment
        attachment = self._create_new_attachment()
        self._add_attachment_to_proj(proj, attachment)

        # Arrange: Create project by repo
        proj_from_repo = await repo.create(proj)

        # Assert: Check if the proj as expected
        assert proj_from_repo.id == proj.id
        assert proj_from_repo.get_attachment_by_id(attachment.id) is not None

    async def test_project_model_create_domain_with_invalid_field_by_repo(self, repo):
        # Arrange: Create Project Domain
        proj = ProjectDomainFactory()
        setattr(proj, "invalid", "invalid")

        # Arrange: Add attachment
        attachment = self._create_new_attachment()
        self._add_attachment_to_proj(proj, attachment)

        # Arrange: Create project by repo
        proj_from_repo = await repo.create(proj)

        # Assert: Check if the proj as expected
        assert hasattr(proj_from_repo, "invalid") is False

    async def test_project_model_update_by_repo(self, repo, default_proj):
        # Arrange: Define attrs
        updated_attrs = {"name": "This is updated names"}

        # Act: Update the project domain model
        for k, v in updated_attrs.items():
            setattr(default_proj, k, v)

        # Act: Update by repo
        updated_proj = await repo.update(default_proj)

        # Assert: Check if update successfully or not
        assert all(getattr(updated_proj, k) == v for k, v in updated_attrs.items())

    async def test_project_model_add_new_attachments_by_repo(
        self, session, repo, default_proj
    ):
        # Arrange: Add new attachments
        NEW_ATTCHMENTS = 5
        new_attchments = []
        for _ in range(NEW_ATTCHMENTS):
            attachment = self._create_new_attachment()
            new_attchments.append(attachment)
            self._add_attachment_to_proj(default_proj, attachment)

        # Act: Update by repo
        updated_proj = await repo.update(default_proj)

        # Assert: Check if update successfully or not
        assert all(
            updated_proj.get_attachment_by_id(attachment.id) is not None
            for attachment in new_attchments
        )

        # Assert: Ensure the attachments are in db
        for attachment in new_attchments:
            result = await session.get(
                Attachment, attachment.id, populate_existing=True
            )
            assert result is not None

    async def test_project_model_remove_attachments_by_repo(self, repo, default_proj):
        # Arrange: Add new attachments
        NEW_ATTCHMENTS = 5
        new_attchments = []
        for _ in range(NEW_ATTCHMENTS):
            attachment = self._create_new_attachment()
            new_attchments.append(attachment)
            self._add_attachment_to_proj(default_proj, attachment)

        # Arrange: Update by repo
        updated_proj = await repo.update(default_proj)

        # Act: Update one attachment
        remove_attachment = new_attchments[0]
        updated_proj.remove_attachment_by_id(remove_attachment.id)

        final_proj = await repo.update(updated_proj)

        # Assert: The remove attachment should not existed, raise ValueError
        with pytest.raises(ValueError):
            final_proj.get_attachment_by_id(remove_attachment.id)

    async def test_project_model_get_by_repo(self, repo, default_proj):
        # Act: Update by repo
        get_proj = await repo.get_by_id(default_proj.id)

        # Assert: Check if update successfully or not
        assert get_proj == default_proj

    async def test_project_model_list_owned_by_repo(self, repo, default_proj):
        # Arrange: Create projects belong to the same account
        owner_id = default_proj.owner_id

        NEW_PROJECTS = 5
        new_projects = []
        for _ in range(NEW_PROJECTS):
            new_projects.append(
                await self._create_project_from_repo(repo, owner_id=owner_id)
            )

        # Act: Get projects owned by the same owner
        projects_from_repo = await repo.list_owned(owner_id)

        assert all(proj in projects_from_repo for proj in new_projects)

import pytest
from dataclasses import asdict

from src.api.domain import ProjectDomain, AttachmentDomain
from src.api.model import Attachment
from src.api.repo import ProjectRepo
from tests.factory.domains import ProjectDomainFactory, AttachmentDomainFactory
from tests.factory.repo import create_project
from src.api.utils import generate_id


class TestProjectModelCase:
    @pytest.fixture(name="repo", scope="function")
    def _create_repo(self, session):
        return ProjectRepo(session)

    def _create_new_attachment(self, **kwargs) -> AttachmentDomain:
        return AttachmentDomainFactory(**kwargs)

    def _add_attachment_to_proj(
        self, proj: ProjectDomain, attachment: AttachmentDomain
    ):
        proj.add_attachment(**asdict(attachment))

    # === HAPPY tests following ===

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

    async def test_project_model_update_by_repo(self, repo, default_project):
        # Arrange: Define attrs
        updated_attrs = {"name": "This is updated names"}

        # Act: Update the project domain model
        for k, v in updated_attrs.items():
            setattr(default_project, k, v)

        # Act: Update by repo
        updated_proj = await repo.update(default_project)

        # Assert: Check if update successfully or not
        assert all(getattr(updated_proj, k) == v for k, v in updated_attrs.items())

    async def test_project_model_add_new_attachments_by_repo(
        self, session, repo, default_project
    ):
        # Arrange: Add new attachments
        NEW_ATTCHMENTS = 5
        new_attchments = []
        for _ in range(NEW_ATTCHMENTS):
            attachment = self._create_new_attachment()
            new_attchments.append(attachment)
            self._add_attachment_to_proj(default_project, attachment)

        # Act: Update by repo
        updated_proj = await repo.update(default_project)

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

    async def test_project_model_remove_attachments_by_repo(
        self, repo, default_project
    ):
        # Arrange: Add new attachments
        NEW_ATTCHMENTS = 5
        new_attchments = []
        for _ in range(NEW_ATTCHMENTS):
            attachment = self._create_new_attachment()
            new_attchments.append(attachment)
            self._add_attachment_to_proj(default_project, attachment)

        # Arrange: Update by repo
        updated_proj = await repo.update(default_project)

        # Act: Update one attachment
        remove_attachment = new_attchments[0]
        updated_proj.remove_attachment_by_id(remove_attachment.id)

        final_proj = await repo.update(updated_proj)

        # Assert: The remove attachment should not existed, raise ValueError
        with pytest.raises(ValueError):
            final_proj.get_attachment_by_id(remove_attachment.id)

    async def test_project_model_get_by_repo(self, repo, default_project):
        # Act: Get by repo
        get_proj = await repo.get_by_id(default_project.id)

        # Assert: Check if get proj as expected
        assert get_proj == default_project

    async def test_project_model_list_by_owner_id_by_repo(self, repo, default_project):
        # Arrange: Create projects belong to the same account
        owner_id = default_project.owner_id

        NEW_PROJECTS = 5
        new_projects = []
        for _ in range(NEW_PROJECTS):
            new_projects.append(await create_project(repo, owner_id=owner_id))

        # Act: Get projects owned by the same owner
        projects_from_repo = await repo.list_by_owner_id(owner_id)

        assert all(proj in projects_from_repo for proj in new_projects)

    async def test_project_model_remove_by_repo(self, repo, default_project):
        # Arrange: Get by repo
        get_proj = await repo.get_by_id(default_project.id)

        # Arrange: Check if get proj as expected
        assert get_proj == default_project

        # Act: Delete the proj by repo
        await repo.delete_by_id(default_project.id)

        # Assert: Delete proj should not be got, raise ValueError
        with pytest.raises(ValueError):
            await repo.get_by_id(default_project.id)

    # === SAD tests following ===

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

    async def test_project_model_create_domain_missing_required_field_by_repo(
        self, repo
    ):
        # Arrange: Remove required attr
        proj = ProjectDomainFactory()
        delattr(proj, "name")

        # Arrange: Create project missing required field by repo should raise AttributeError
        with pytest.raises(AttributeError):
            await repo.create(proj)

    async def test_project_model_update_with_invalid_field_by_repo(
        self, repo, default_project
    ):
        # Arrange: Define attrs
        updated_attrs = {"invalid": "This is invalid"}

        # Act: Update the project domain model
        for k, v in updated_attrs.items():
            setattr(default_project, k, v)

        # Act: Update by repo
        updated_proj = await repo.update(default_project)

        # Assert: Check if update successfully or not
        assert all(hasattr(updated_proj, k) is False for k in updated_attrs.keys())

    async def test_project_model_update_domain_missing_required_field_by_repo(
        self, repo, default_project
    ):
        # Arrange: Remove required attr
        delattr(default_project, "name")

        # Arrange: Update project missing required field by repo should raise AttributeError
        with pytest.raises(AttributeError):
            await repo.update(default_project)

    async def test_project_model_remove_non_existed_project_by_repo(
        self, repo, default_project
    ):
        # Assert: Delete non-existed proj should raise ValueError
        with pytest.raises(ValueError):
            await repo.delete_by_id(generate_id())

    async def test_project_model_get_non_existed_project_by_repo(
        self, repo, default_project
    ):
        # Assert: Get non-existed proj should raise ValueError
        with pytest.raises(ValueError):
            await repo.get_by_id(generate_id())

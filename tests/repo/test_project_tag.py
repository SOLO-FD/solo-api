import pytest

from src.api.repo import ProjectRepo, TagRepo
from src.api.model import ProjectTagAssociation
from tests.factory.repo import create_project, create_tag


class TestProjectTagModelCase:
    @pytest.fixture(name="project_repo", scope="function")
    def _create_project_repo(self, session):
        return ProjectRepo(session)

    @pytest.fixture(name="tag_repo", scope="function")
    def _create_tag_repo(self, session):
        return TagRepo(session)

    # === HAPPY tests following ===
    async def test_project_add_tag_by_repo(
        self, session, project_repo, default_project, default_tag
    ):
        # Arrange: Add tag to project
        await project_repo.add_tag_by_id(default_project.id, default_tag.id)

        # Assert: Check if the association saved in db
        assoc = await session.get(
            ProjectTagAssociation,
            {"project_id": default_project.id, "tag_id": default_tag.id},
            populate_existing=True,
        )
        assert assoc is not None

    async def test_project_remove_tag_by_repo(
        self, session, project_repo, default_project, default_tag
    ):
        # Arrange: Add tag to project
        await project_repo.add_tag_by_id(default_project.id, default_tag.id)

        # Act: Remove the tag from the project
        await project_repo.remove_tag_by_id(default_project.id, default_tag.id)

        # Assert: Check if the association removed from db
        assoc = await session.get(
            ProjectTagAssociation,
            {"project_id": default_project.id, "tag_id": default_tag.id},
            populate_existing=True,
        )
        assert assoc is None

    async def test_project_list_by_tag_id_by_repo(self, project_repo, default_tag):
        # Arrange: Create projects, and add default_tag
        NEW_PROJECTS = 5
        new_projects = []
        for _ in range(NEW_PROJECTS):
            proj = await create_project(project_repo)
            new_projects.append(proj)
            await project_repo.add_tag_by_id(proj.id, default_tag.id)

        # Act: Get projects by tag_id
        projects_from_repo = await project_repo.list_by_tag_id(default_tag.id)

        # Assert: Check all new projects included
        assert all(proj in projects_from_repo for proj in new_projects)

    async def test_tag_list_by_project_id_by_repo(
        self, tag_repo, project_repo, default_project
    ):
        # Arrange: Create tags, and add default_project
        NEW_TAGS = 5
        new_tags = []
        for _ in range(NEW_TAGS):
            tag = await create_tag(tag_repo)
            new_tags.append(tag)
            await project_repo.add_tag_by_id(default_project.id, tag.id)

        # Act: Get tags by project_id
        tags_from_repo = await tag_repo.list_by_project_id(default_project.id)

        # Assert: Check all new projects included
        assert all(tag in tags_from_repo for tag in new_tags)

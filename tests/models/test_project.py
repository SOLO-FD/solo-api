from src.api.models import Project
from tests.factories.models import ProjectFactory


class TestProjectModelCase:
    async def test_project_model_create(self, session):
        # Arrange: Define param
        project_param = {
            "name": "Good Project",
            "header_url": "https://example.com/awesome-pic",
        }

        project = ProjectFactory(**project_param)

        # Act: Create project orm
        session.add(project)
        await session.commit()
        await session.refresh(project)

        # Assert: Test if successfully create orm
        assert project is not None
        assert all(
            getattr(project, name) == value for name, value in project_param.items()
        )

    async def test_project_model_update(self, default_project, session):
        # Arrange: Update param
        updated_param = {
            "name": "Updated Project",
        }

        # Act: Update project orm
        for name, value in updated_param.items():
            setattr(default_project, name, value)

        await session.commit()
        await session.refresh(default_project)

        # Assert: Test if successfully update orm
        assert all(
            getattr(default_project, name) == value
            for name, value in updated_param.items()
        )

    async def test_project_model_get(self, default_project, session):
        # Act: Get project by session
        project_from_db = await session.get(Project, default_project.id)

        # Assert: Test if successfully get orm from db
        assert project_from_db == default_project

    async def test_project_model_delete(self, default_project, session):
        # Act: Delete project by session
        await session.delete(default_project)
        await session.commit()

        # Assert: Test if successfully get orm from db
        assert await session.get(Project, default_project.id) is None

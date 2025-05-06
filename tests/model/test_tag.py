from sqlalchemy import select

from src.api.model import Tag, Project, ProjectTagAssociation
from tests.factory.models import TagFactory, ProjectFactory


class TestTagModelCase:
    async def test_tag_model_create(self, session):
        # Arrange: Define param
        tag_param = {
            "name": "Good Tag",
            "color": "#FFFFFF",
        }

        tag = TagFactory(**tag_param)

        # Act: Create tag orm
        session.add(tag)
        await session.commit()
        await session.refresh(tag)

        # Assert: Test if successfully create orm
        assert tag is not None
        assert all(getattr(tag, name) == value for name, value in tag_param.items())

    async def test_tag_model_update(self, default_tag, session):
        # Arrange: Update param
        updated_param = {
            "name": "Updated Tag",
        }

        # Act: Update tag orm
        for name, value in updated_param.items():
            setattr(default_tag, name, value)

        await session.commit()
        await session.refresh(default_tag)

        # Assert: Test if successfully update orm
        assert all(
            getattr(default_tag, name) == value for name, value in updated_param.items()
        )

    async def test_tag_model_get(self, default_tag, session):
        # Act: Get tag by session
        tag_from_db = await session.get(Tag, default_tag.id)

        # Assert: Test if successfully get orm from db
        assert tag_from_db == default_tag

    async def test_tag_model_delete(self, default_tag, session):
        # Act: Delete tag by session
        await session.delete(default_tag)
        await session.commit()

        # Assert: Test if successfully get orm from db
        assert await session.get(Tag, default_tag.id) is None

    async def test_get_projects_from_tag(self, default_tag, session):
        # Arrange: Create projects and associations
        NEW_PROJECT = 5
        project_ids = []
        for _ in range(NEW_PROJECT):
            proj = ProjectFactory()
            project_ids.append(proj.id)
            assoc = ProjectTagAssociation(project=proj, tag=default_tag)
            session.add_all([proj, assoc])

        # Arrange: Check id includes
        assert len(project_ids) == NEW_PROJECT

        await session.commit()

        # Arrange: Get tag from database
        tag_from_db = await session.get(
            Tag,
            default_tag.id,
            populate_existing=True,
        )

        # Act: Get projects from database
        result = await session.scalars(tag_from_db.projects.select())
        proj_ids_from_db = [assoc.project_id for assoc in result.all()]
        results = await session.scalars(
            select(Project).where(Project.id.in_(proj_ids_from_db))
        )

        # Assert: Check if all id included
        assert all(proj.id in project_ids for proj in results.all())

from src.api.models import Project, Attachment, ProjectTagAssociation
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
        project_from_db = await session.get(
            Project,
            default_project.id,
        )

        # Assert: Test if successfully get orm from db
        assert project_from_db == default_project

    async def test_project_model_delete(self, default_project, session):
        # Act: Delete project by session
        await session.delete(default_project)
        await session.commit()

        # Assert: Test if successfully get orm from db
        assert (
            await session.get(
                Project,
                default_project.id,
            )
            is None
        )

    async def test_project_still_there_when_attachment_deleted(
        self, default_project, default_attachment, session
    ):
        # Arrange: Add default attachment to default project
        default_project.attachments.add(default_attachment)
        await session.commit()
        await session.refresh(default_project)

        # Arrange: Ensure the attachment is added to project

        result = await session.scalars(
            default_project.attachments.select().where(
                Attachment.id == default_attachment.id
            )
        )

        assert result.one() is not None

        # Act: Delete Attachment
        await session.delete(default_attachment)
        await session.commit()

        # Assert: Attachment should be disappeared as well
        assert (
            await session.get(
                Project,
                default_project.id,
                populate_existing=True,
            )
            is not None
        )

    async def test_project_add_tag(self, default_project, default_tag, session):
        # Arrange: Create association
        assoc = ProjectTagAssociation(project=default_project, tag=default_tag)

        # Act: Add to database
        session.add(assoc)
        await session.commit()

        # Arrange: Get project from database
        project_from_db = await session.get(
            Project,
            default_project.id,
            populate_existing=True,
        )

        # Act: Get assoc from database
        result = await session.scalars(
            project_from_db.tags.select().where(
                ProjectTagAssociation.tag_id == default_tag.id
            )
        )
        tag_assoc = result.one_or_none()

        # Assert: Default tag should be included
        assert tag_assoc is not None

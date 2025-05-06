import pytest
from sqlalchemy.exc import IntegrityError
from src.api.model import Attachment, Project
from tests.factory.models import AttachmentFactory


class TestAttachmentModelCase:
    async def test_attachment_model_create(self, session):
        # Arrange: Define param
        attachment_param = {
            "filename": "Good Attachment",
            "url": "https://example.com/awesome-pic",
        }

        attachment = AttachmentFactory(**attachment_param)

        # Act: Create attachment orm
        session.add(attachment)
        await session.commit()
        await session.refresh(attachment)

        # Assert: Test if successfully create orm
        assert attachment is not None
        assert all(
            getattr(attachment, name) == value
            for name, value in attachment_param.items()
        )

    async def test_attachment_model_update(self, default_attachment, session):
        # Arrange: Update param
        updated_param = {
            "filename": "Updated Attachment",
        }

        # Act: Update attachment orm
        for name, value in updated_param.items():
            setattr(default_attachment, name, value)

        await session.commit()
        await session.refresh(default_attachment)

        # Assert: Test if successfully update orm
        assert all(
            getattr(default_attachment, name) == value
            for name, value in updated_param.items()
        )

    async def test_attachment_model_get(self, default_attachment, session):
        # Act: Get attachment by session
        attachment_from_db = await session.get(
            Attachment,
            default_attachment.id,
        )

        # Assert: Test if successfully get orm from db
        assert attachment_from_db == default_attachment

    async def test_attachment_model_delete(self, default_attachment, session):
        # Act: Delete attachment by session
        await session.delete(default_attachment)
        await session.commit()

        # Assert: Test if successfully get orm from db
        assert (
            await session.get(
                Attachment,
                default_attachment.id,
            )
            is None
        )

    async def test_attachemnt_without_project(self, session):
        # Arrange: Define param
        attachment_param = {
            "filename": "Good Attachment",
            "url": "https://example.com/awesome-pic",
            "project": None,
            "project_id": "",
        }

        attachment = AttachmentFactory(**attachment_param)

        # Act: Add attachment
        session.add(attachment)

        # Assert: Attachment without project will raise IntegrityError
        with pytest.raises(IntegrityError):
            await session.commit()

    async def test_attachemnt_by_passing_project(self, session, default_project):
        # Arrange: Define param
        attachment_param = {
            "filename": "Good Attachment",
            "url": "https://example.com/awesome-pic",
            "project": None,
            "project_id": "",
        }

        attachment = AttachmentFactory(**attachment_param)

        # Act: Passing project
        attachment.project = default_project

        # Act: Add attachment
        session.add(attachment)
        await session.commit()

        # Assert: Attachment should be in project's collection
        results = await session.scalars(
            default_project.attachments.select().where(Attachment.id == attachment.id)
        )
        attachment = results.one()
        assert attachment is not None

    async def test_attachemnt_by_passing_project_id(self, session, default_project):
        # Arrange: Define param
        attachment_param = {
            "filename": "Good Attachment",
            "url": "https://example.com/awesome-pic",
            "project": None,
            "project_id": "",
        }

        attachment = AttachmentFactory(**attachment_param)

        # Act: Passing project
        attachment.project_id = default_project.id

        # Act: Add attachment
        session.add(attachment)

        # Assert: Attachment passed project_id will raise IntegrityError
        with pytest.raises(IntegrityError):
            await session.commit()

    async def test_attachment_deleted_when_project_deleted(
        self, default_attachment, session
    ):
        # Arrange: Get project from attachment
        proj = await session.get(
            Project,
            default_attachment.project_id,
        )

        # Act: Delete Project
        await session.delete(proj)
        await session.commit()

        # Assert: Attachment should be disappeared as well

        assert (
            await session.get(
                Project,
                default_attachment.project_id,
                populate_existing=True,
            )
            is None
        )

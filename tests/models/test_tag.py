from src.api.models import Tag
from tests.factories.models import TagFactory


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

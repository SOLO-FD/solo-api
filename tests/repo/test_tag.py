import pytest

from tests.factory.repo import create_tag
from tests.factory.domains import TagDomainFactory
from src.api.utils import generate_id


class TestTagModelCase:
    # === HAPPY tests following ===

    async def test_tag_model_create_by_repo(self, tag_repo):
        # Arrange: Create Tag Domain
        tag = TagDomainFactory()

        # Arrange: Create tag by repo
        tag_from_repo = await tag_repo.create(tag)

        # Assert: Check if the tag as expected
        assert tag_from_repo.id == tag.id

    async def test_tag_model_update_by_repo(self, tag_repo, default_tag):
        # Arrange: Define attrs
        updated_attrs = {"name": "This is updated names"}

        # Act: Update the tag domain model
        for k, v in updated_attrs.items():
            setattr(default_tag, k, v)

        # Act: Update by repo
        updated_tag = await tag_repo.update(default_tag)

        # Assert: Check if update successfully or not
        assert all(getattr(updated_tag, k) == v for k, v in updated_attrs.items())

    async def test_tag_model_get_by_repo(self, tag_repo, default_tag):
        # Act: Get by repo
        get_tag = await tag_repo.get_by_id(default_tag.id)

        # Assert: Check if get tag as expected
        assert get_tag == default_tag

    async def test_tag_model_list_by_owner_id_by_repo(self, tag_repo, default_tag):
        # Arrange: Create tags belong to the same account
        owner_id = default_tag.owner_id

        NEW_TAGS = 5
        new_tags = []
        for _ in range(NEW_TAGS):
            new_tags.append(await create_tag(tag_repo, owner_id=owner_id))

        # Act: Get tags owned by the same owner
        tags_from_repo = await tag_repo.list_by_owner_id(owner_id)

        assert all(tag in tags_from_repo for tag in new_tags)

    async def test_tag_model_get_ids_by_repo(self, tag_repo, default_tag):
        # Arrange: Create tags
        NEW_TAGS = 5
        new_tags = []
        for _ in range(NEW_TAGS):
            new_tags.append(await create_tag(tag_repo))

        # Act: Get tags owned by the same owner
        tags_from_repo = await tag_repo.get_by_ids([proj.id for proj in new_tags])
        assert all(proj in tags_from_repo for proj in new_tags)

    async def test_tag_model_remove_by_repo(self, tag_repo, default_tag):
        # Arrange: Get by repo
        get_tag = await tag_repo.get_by_id(default_tag.id)

        # Arrange: Check if get tag as expected
        assert get_tag == default_tag

        # Act: Delete the tag by repo
        await tag_repo.delete_by_id(default_tag.id)

        # Assert: Delete tag should not be got, raise ValueError
        with pytest.raises(ValueError):
            await tag_repo.get_by_id(default_tag.id)

    # === SAD tests following ===

    async def test_tag_model_create_domain_with_invalid_field_by_repo(self, tag_repo):
        # Arrange: Create Tag Domain
        tag = TagDomainFactory()
        setattr(tag, "invalid", "invalid")

        # Arrange: Create tag by repo
        tag_from_repo = await tag_repo.create(tag)

        # Assert: Check if the tag as expected
        assert hasattr(tag_from_repo, "invalid") is False

    async def test_tag_model_create_domain_missing_required_field_by_repo(
        self, tag_repo
    ):
        # Arrange: Remove required attr
        tag = TagDomainFactory()
        delattr(tag, "name")

        # Arrange: Create tag missing required field by repo should raise AttributeError
        with pytest.raises(AttributeError):
            await tag_repo.create(tag)

    async def test_tag_model_update_with_invalid_field_by_repo(
        self, tag_repo, default_tag
    ):
        # Arrange: Define attrs
        updated_attrs = {"invalid": "This is invalid"}

        # Act: Update the tag domain model
        for k, v in updated_attrs.items():
            setattr(default_tag, k, v)

        # Act: Update by repo
        updated_tag = await tag_repo.update(default_tag)

        # Assert: Check if update successfully or not
        assert all(hasattr(updated_tag, k) is False for k in updated_attrs.keys())

    async def test_tag_model_update_domain_missing_required_field_by_repo(
        self, tag_repo, default_tag
    ):
        # Arrange: Remove required attr
        delattr(default_tag, "name")

        # Arrange: Update tag missing required field by repo should raise AttributeError
        with pytest.raises(AttributeError):
            await tag_repo.update(default_tag)

    async def test_tag_model_remove_non_existed_tag_by_repo(
        self, tag_repo, default_tag
    ):
        # Assert: Delete non-existed tag should raise ValueError
        with pytest.raises(ValueError):
            await tag_repo.delete_by_id(generate_id())

    async def test_tag_model_get_non_existed_tag_by_repo(self, tag_repo, default_tag):
        # Assert: Get non-existed tag should raise ValueError
        with pytest.raises(ValueError):
            await tag_repo.get_by_id(generate_id())

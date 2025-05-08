import pytest
from dataclasses import asdict

from api.service import TagService
from api.dto import (
    TagCreateDTO,
    TagUpdateDTO,
)
from api.domain import TagDomain
from api.utils import generate_id
from tests.factory.domains import TagDomainFactory
from tests.factory.dto import new_dto_from_domain_factory
from tests.factory.service import create_tag_by_service


class TestTagServiceCase:
    # === HAPPY tests following ===
    async def test_create_tag_by_service(self, session):
        # Arrange: Create tag create DTO
        tag_dto = new_dto_from_domain_factory(
            TagDomainFactory,
            TagCreateDTO,
        )

        # Act: Create tag by service
        service = TagService(session)
        fake_id = generate_id()

        tag_return = await service.create(fake_id, tag_dto)

        # Assert: Assert Correct type
        assert isinstance(tag_return, TagDomain)

        # Assert: Core attributes match
        expected_dict = tag_dto.model_dump()
        actual_dict = asdict(tag_return)

        for key, expected_val in expected_dict.items():
            assert actual_dict[key] == expected_val, f"Mismatch on '{key}'"

    async def test_update_tag_by_service(self, session, new_tag):
        # Arrange: Create a tag update dto
        update_param = {"name": "This is update name!"}
        updated_dto = TagUpdateDTO(**update_param)

        # Act: Update tag by service
        service = TagService(session)
        tag_return = await service.update(new_tag.owner_id, new_tag.id, updated_dto)

        # Assert: Check if the updated success
        return_dict = asdict(tag_return)
        assert all(return_dict[k] == v for k, v in update_param.items())

    async def test_get_tag_by_service(self, session, new_tag):
        # Act: Get tag by service
        service = TagService(session)
        tag_return = await service.get_by_id(new_tag.owner_id, new_tag.id)

        # Assert: Check if the tag be the same
        assert tag_return == new_tag

    async def test_list_tag_by_service(self, session):
        # Arrange: Generate owner_id
        owner_id = generate_id()
        # Arrange: Create tags by service
        NEW_TAGS = 7
        new_tags = []

        for _ in range(NEW_TAGS):
            tag_return = await create_tag_by_service(session, owner_id=owner_id)
            new_tags.append(tag_return)

        # Act: Get tags
        service = TagService(session)
        tag_list_return = await service.list_by_owner_id(owner_id)

        # Assert: Check if the tag be the same
        assert all(proj in tag_list_return for proj in new_tags)

    async def test_delete_tag_by_service(self, session, new_tag):
        # Act: Delete tag by service
        service = TagService(session)
        await service.delete_by_id(new_tag.owner_id, new_tag.id)

        # Assert: Check if the tag deleted
        with pytest.raises(ValueError):
            await service.get_by_id(new_tag.owner_id, new_tag.id)

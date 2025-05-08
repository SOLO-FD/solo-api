import pytest
from dataclasses import asdict
from fastapi.encoders import jsonable_encoder

from src.api.dto import (
    TagCreateDTO,
    TagUpdateDTO,
    TagPublicDTO,
)
from src.api.repo import TagRepo
from tests.factory.domains import (
    TagDomainFactory,
)


class TestTagAPICase:
    async def test_create_tag_by_api(
        self, session, client, default_header, default_account_id
    ):
        # Arrange: Create a tag payload
        tag = TagDomainFactory(owner_id=default_account_id)
        payload_dict = TagCreateDTO(**asdict(tag)).model_dump()

        # Act: Create resource
        response = client.post(
            "/v1/tags/",
            headers=default_header,
            json=jsonable_encoder(payload_dict),
        )

        # Assert: Check if the action success
        assert response.status_code == 200
        tag_id = response.json()["id"]

        # Assert: Check if the tag add to the db
        repo = TagRepo(session)
        db_tag = await repo.get_by_id(tag_id)

        # All the giving attr in TagPublicDTO should be in the tag returned from db
        db_tag_dto_dict = TagPublicDTO(**asdict(db_tag)).model_dump()

        for key, value in payload_dict.items():
            assert db_tag_dto_dict[key] == value

    async def test_get_tag_by_api(self, client, default_header, default_tag):
        # Act: Get resource
        response = client.get(
            f"/v1/tags/{default_tag.id}",
            headers=default_header,
        )

        # Assert: Check if the action success
        assert response.status_code == 200

        # Assert: Check the tag fields
        expected_dict = {k: v for k, v in asdict(default_tag).items()}
        return_dto = TagPublicDTO.model_validate(response.json())

        assert all(expected_dict[k] == v for k, v in return_dto.model_dump().items())

    async def test_update_tag_by_api(
        self, session, client, default_header, default_tag
    ):
        # Arrange: Create TagUpdateDTO
        updated_attrs = {
            "name": "This is for tag update",
        }

        tag_id = default_tag.id

        # Act: Update resource
        response = client.patch(
            f"/v1/tags/{tag_id}",
            headers=default_header,
            json=jsonable_encoder(TagUpdateDTO(**updated_attrs).model_dump()),
        )

        # Assert: Check if the action success
        assert response.status_code == 200

        # Assert: Check if the tag updated in db
        repo = TagRepo(session)
        db_tag = await repo.get_by_id(tag_id)

        # All the giving attr in TagPublicDTO should be in the tag returned from db
        for key, value in updated_attrs.items():
            assert getattr(db_tag, key) == value

    async def test_delete_tag_by_api(
        self, session, client, default_header, default_tag
    ):
        # Arrange: Get tag id
        tag_id = default_tag.id

        # Act: Delete resource
        response = client.delete(
            f"/v1/tags/{tag_id}",
            headers=default_header,
        )

        # Assert: Check if the action success
        assert response.status_code == 204

        # Assert: Check if the tag deleted in db
        repo = TagRepo(session)
        with pytest.raises(ValueError):
            await repo.get_by_id(tag_id)

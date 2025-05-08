import pytest
from dataclasses import asdict
from fastapi.encoders import jsonable_encoder

from src.api.dto import (
    ProjectCreateDTO,
    ProjectUpdateDTO,
    ProjectPublicDTO,
)
from src.api.repo import ProjectRepo
from tests.factory.domains import (
    ProjectDomainFactory,
    AttachmentDomainFactory,
)


class TestProjectAPICase:
    async def test_create_project_by_api(
        self, session, client, default_header, default_account_id
    ):
        # Arrange: Create a project payload
        proj = ProjectDomainFactory(owner_id=default_account_id)
        payload_dict = ProjectCreateDTO(**asdict(proj)).model_dump()

        # Act: Create resource
        response = client.post(
            "/v1/projects/",
            headers=default_header,
            json=jsonable_encoder(payload_dict),
        )

        # Assert: Check if the action success
        assert response.status_code == 200
        proj_id = response.json()["id"]

        # Assert: Check if the project add to the db
        repo = ProjectRepo(session)
        db_project = await repo.get_by_id(proj_id)

        # All the giving attr in ProjectPublicDTO should be in the proj returned from db
        db_project_dto_dict = ProjectPublicDTO(**asdict(db_project)).model_dump()

        for key, value in payload_dict.items():
            assert db_project_dto_dict[key] == value

    async def test_get_project_by_api(self, client, default_header, default_project):
        # Act: Get resource
        response = client.get(
            f"/v1/projects/{default_project.id}",
            headers=default_header,
        )

        # Assert: Check if the action success
        assert response.status_code == 200

        # Assert: Check the project fields (exclude attachments)
        drop_keys = {"attachments"}
        expected_dict = {
            k: v for k, v in asdict(default_project).items() if k not in drop_keys
        }
        return_dto = ProjectPublicDTO.model_validate(response.json())

        assert all(
            expected_dict[k] == v
            for k, v in return_dto.model_dump(exclude=drop_keys).items()
        )

        # Assert: Check attachment values
        expected_attachment_dict = {
            attachment.checksum: asdict(attachment)
            for attachment in default_project.attachments
        }
        return_attachment_dict = {
            attachment.checksum: attachment.model_dump()
            for attachment in return_dto.attachments
        }

        for checksum, attachment in expected_attachment_dict.items():
            assert attachment == return_attachment_dict[checksum]

    async def test_update_project_by_api(
        self, session, client, default_header, default_project
    ):
        # Arrange: Create ProjectUpdateDTO
        updated_attrs = {
            "name": "This is for project update",
        }

        proj_id = default_project.id

        # Act: Update resource
        response = client.patch(
            f"/v1/projects/{proj_id}",
            headers=default_header,
            json=jsonable_encoder(ProjectUpdateDTO(**updated_attrs).model_dump()),
        )

        # Assert: Check if the action success
        assert response.status_code == 200

        # Assert: Check if the project updated in db
        repo = ProjectRepo(session)
        db_project = await repo.get_by_id(proj_id)

        # All the giving attr in ProjectPublicDTO should be in the proj returned from db
        for key, value in updated_attrs.items():
            assert getattr(db_project, key) == value

    async def test_add_attachment_in_project_by_api(
        self, session, client, default_header, default_project
    ):
        # Arrange: Create New Attachment
        NEW_ATTACHMENTS = 3
        new_attachments = []

        for _ in range(NEW_ATTACHMENTS):
            attachment = AttachmentDomainFactory()
            new_attachments.append(asdict(attachment))

        updated_attrs = {
            "attachments": new_attachments,
        }

        updated_dto_dict = ProjectUpdateDTO(**updated_attrs).model_dump()

        proj_id = default_project.id

        # Act: Update resource
        response = client.patch(
            f"/v1/projects/{proj_id}",
            headers=default_header,
            json=jsonable_encoder(updated_dto_dict),
        )

        # Assert: Check if the action success
        assert response.status_code == 200

        # Assert: Check if the project updated in db
        repo = ProjectRepo(session)
        db_project = await repo.get_by_id(proj_id)

        expected_attachments_dict = {
            attachment["checksum"]: attachment
            for attachment in updated_dto_dict["attachments"]
        }
        return_attachments_dict = {
            attachment.checksum: asdict(attachment)
            for attachment in db_project.attachments
        }

        # All the giving attr in ProjectPublicDTO should be in the proj returned from db
        for checksum, expected_dict in expected_attachments_dict.items():
            return_attachment_dict = return_attachments_dict[checksum]
            for key, value in expected_dict.items():
                assert return_attachment_dict[key] == value

    async def test_delete_project_by_api(
        self, session, client, default_header, default_project
    ):
        # Arrange: Get project id
        proj_id = default_project.id

        # Act: Delete resource
        response = client.delete(
            f"/v1/projects/{proj_id}",
            headers=default_header,
        )

        # Assert: Check if the action success
        assert response.status_code == 204

        # Assert: Check if the project deleted in db
        repo = ProjectRepo(session)
        with pytest.raises(ValueError):
            await repo.get_by_id(proj_id)

    async def test_remove_attachment_by_api(
        self, session, client, default_header, default_project
    ):
        # Arrange: Get project id and attachment id
        proj_id = default_project.id
        attachment_id = default_project.attachments[0].id

        # Act: Delete resource
        response = client.delete(
            f"/v1/projects/{proj_id}/attachments/{attachment_id}",
            headers=default_header,
        )

        # Assert: Check if the action success
        assert response.status_code == 204

        # Assert: Check if the attachment deleted in db
        repo = ProjectRepo(session)
        proj = await repo.get_by_id(proj_id)

        with pytest.raises(ValueError):
            proj.get_attachment_by_id(attachment_id)

from dataclasses import asdict

from src.api.service import ProjectService
from src.api.dto import (
    ProjectCreateDTO,
    ProjectUpdateDTO,
    AttachmentCreateDTO,
)
from src.api.domain import ProjectDomain

from tests.factory.domains import ProjectDomainFactory, AttachmentDomainFactory
from tests.factory.dto import new_dto_from_domain_factory


class TestProjectServiceCase:
    async def _create_project_by_service(
        self, session, attachment_num=3
    ) -> ProjectDomain:
        project_dto = new_dto_from_domain_factory(
            ProjectDomainFactory,
            ProjectCreateDTO,
        )

        for _ in range(attachment_num):
            attachment_dto = new_dto_from_domain_factory(
                AttachmentDomainFactory,
                AttachmentCreateDTO,
            )
            project_dto.attachments.append(attachment_dto)

        service = ProjectService(session)
        return await service.create(project_dto)

    # === HAPPY tests following ===
    async def test_create_project_by_service(self, session):
        # Arrange: Create project create DTO
        project_dto = new_dto_from_domain_factory(
            ProjectDomainFactory,
            ProjectCreateDTO,
        )

        NEW_ATTACHMENTS = 5
        for _ in range(NEW_ATTACHMENTS):
            attachment_dto = new_dto_from_domain_factory(
                AttachmentDomainFactory,
                AttachmentCreateDTO,
            )
            project_dto.attachments.append(attachment_dto)

        # Act: Create project by service
        service = ProjectService(session)
        project_return = await service.create(project_dto)

        # Assert: Assert Correct type
        assert isinstance(project_return, ProjectDomain)

        # Assert: Core attributes match (exclude attachments for now)
        expected_dict = project_dto.model_dump(exclude={"attachments"})
        actual_dict = asdict(project_return)

        for key, expected_val in expected_dict.items():
            assert actual_dict[key] == expected_val, f"Mismatch on '{key}'"

        # Assert: Attachments match by checksum
        returned_attachments = {
            a.checksum: asdict(a) for a in project_return.attachments
        }
        input_attachments = {
            a.checksum: a.model_dump() for a in project_dto.attachments
        }

        assert returned_attachments.keys() == input_attachments.keys(), (
            "Attachment checksums mismatch"
        )

        for checksum, ret_data in returned_attachments.items():
            input_data = input_attachments[checksum]
            for k, v in input_data.items():
                assert ret_data.get(k) == v, (
                    f"Mismatch on attachment '{checksum}' key '{k}'"
                )

    async def test_update_project_by_service(self, session):
        # Arrange: Create a project
        new_project = await self._create_project_by_service(session)

        # Arrange: Create a project update dto
        update_param = {"name": "This is update name!"}
        updated_dto = ProjectUpdateDTO(**update_param)

        # Act: Update project by service
        service = ProjectService(session)
        project_return = await service.update(new_project.id, updated_dto)

        # Assert: Check if the updated success
        return_dict = asdict(project_return)
        assert all(return_dict[k] == v for k, v in update_param.items())

    async def test_add_attachment_by_service(self, session):
        # Arrange: Create a project
        new_project = await self._create_project_by_service(session)

        # Arrange: Create new attachments
        NEW_ATTACHMENTS = 3
        attachment_list = []
        for _ in range(NEW_ATTACHMENTS):
            new_attachment = new_dto_from_domain_factory(
                AttachmentDomainFactory, AttachmentCreateDTO
            )
            attachment_list.append(new_attachment)

        # Arrange: Create update DTO
        updated_dto = ProjectUpdateDTO(attachments=attachment_list)

        # Act: Update project by service
        service = ProjectService(session)
        project_return = await service.update(new_project.id, updated_dto)

        # Assert: Check if the updated success
        dto_attachments = {a.checksum: a.model_dump() for a in updated_dto.attachments}
        return_attachments = {a.checksum: asdict(a) for a in project_return.attachments}

        # Check all new attachments added
        assert set(dto_attachments.keys()).issubset(set(return_attachments.keys()))

        # Check if all attachments are hold the same info
        for key, attachment in dto_attachments.items():
            return_attachment = return_attachments[key]
            assert all(return_attachment[k] == v for k, v in attachment.items())

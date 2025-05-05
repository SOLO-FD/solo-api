import pytest
from tests.factories.domains import AttachmentDomainFactory
from src.api.utils import generate_id


class TestProjectDomainCase:
    def _add_new_attachment_to_project(self, proj):
        a = AttachmentDomainFactory()
        attrs = {
            "filename": a.filename,
            "file_type": a.file_type,
            "url": a.url,
            "size": a.size,
            "checksum": a.checksum,
        }

        return proj.add_attachment(**attrs)

    def test_project_domain_add_attachment(self, default_project):
        # Arrange: Create attachment param
        a = AttachmentDomainFactory()
        attrs = {
            "filename": a.filename,
            "file_type": a.file_type,
            "url": a.url,
            "size": a.size,
            "checksum": a.checksum,
        }

        # Act: Add attachment
        a_return = default_project.add_attachment(**attrs)

        # Assert: Attachment is in default_project
        assert a_return.id in [a.id for a in default_project.attachments]

    def test_project_domain_get_attachments(self, default_project):
        # Arrange: Add attachments
        NEW_ATTACHMENTS = 5
        attachment_list = []
        for _ in range(NEW_ATTACHMENTS):
            attachment_list.append(self._add_new_attachment_to_project(default_project))

        attachments_from_prof = default_project.attachments

        assert all(a in attachment_list for a in attachments_from_prof)

    def test_project_domain_get_attachment_by_id(self, default_project):
        # Arrange: Add attachment
        attachment = self._add_new_attachment_to_project(default_project)

        assert attachment is default_project.get_attachment_by_id(attachment.id)

    def test_project_domain_delete_attachment_by_id(self, default_project):
        # Arrange: Add attachment
        attachment = self._add_new_attachment_to_project(default_project)
        assert attachment is default_project.get_attachment_by_id(attachment.id)

        # Act: Remove attachment
        default_project.remove_attachment_by_id(attachment.id)

        # Assert: Try get the removed attachment should rasie ValueError
        with pytest.raises(ValueError):
            default_project.get_attachment_by_id(attachment.id)

    def test_project_domain_add_attachment_missing_requird_field(self, default_project):
        # Arrange: Create attachment param
        a = AttachmentDomainFactory()
        attrs = {
            "filename": a.filename,
            "file_type": a.file_type,
            "url": a.url,
            "size": a.size,
        }

        # Assert: Add attachment missing required field should failed
        with pytest.raises(TypeError):
            default_project.add_attachment(**attrs)

    def test_project_domain_add_attachment_with_invalid_field(self, default_project):
        # Arrange: Create attachment param
        a = AttachmentDomainFactory()
        attrs = {
            "filename": a.filename,
            "file_type": a.file_type,
            "url": a.url,
            "size": a.size,
            "checksum": a.checksum,
            "invalid_field": "invalid",
        }

        # Act: Add attachment with invalid field
        a_return = default_project.add_attachment(**attrs)

        # Assert: Attachment is in default_project
        assert hasattr(a_return, "invalid_field") is False

    def test_project_domain_get_non_existed_attachment_by_id(self, default_project):
        # Assert: Try get non-existed attachment should rasie ValueError
        with pytest.raises(ValueError):
            default_project.get_attachment_by_id(generate_id())

    def test_project_domain_delete_non_existed_attachment_by_id(self, default_project):
        # Assert: Try remove non-existed attachment should rasie ValueError
        with pytest.raises(ValueError):
            default_project.remove_attachment_by_id(generate_id())

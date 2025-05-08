from dataclasses import dataclass, field
from datetime import date
from typing import Optional, get_type_hints
from .base import EntityDomain
from .attachment import AttachmentDomain


@dataclass(kw_only=True)
class ProjectDomain(EntityDomain):
    start_date: date
    end_date: Optional[date] = None
    header_url: Optional[str] = None
    cover_url: Optional[str] = None
    _attachments: list[AttachmentDomain] = field(default_factory=list)

    @property
    def attachments(self) -> list[AttachmentDomain]:
        return self._attachments

    def __repr__(self) -> str:
        if len(self._attachments) > 1:
            unit = "attachments"
        else:
            unit = "attachment"
        return f"<ProjectDomain(id='{self.id}', name='{self.name}, {len(self._attachments)} {unit}')>"

    def add_attachment(self, **kwargs) -> AttachmentDomain:
        # Only allow valid fields from AttachmentDomain

        allowed_keys = set(get_type_hints(AttachmentDomain).keys())
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_keys}

        # Instanced attachment
        attachment = AttachmentDomain(**filtered_kwargs)

        self._attachments.append(attachment)
        return attachment

    def add_attachments(self, items: list[dict]) -> list[AttachmentDomain]:
        attachment_list = []
        for item in items:
            attachment_list.append(self.add_attachment(**item))

        return attachment_list

    def get_attachment_by_id(self, attachment_id: str) -> Optional[AttachmentDomain]:
        matches = [a for a in self._attachments if a.id == attachment_id]
        if len(matches) > 1:
            raise ValueError(
                f"Attachment with id={attachment_id} should be unique, found {len(matches)}."
            )

        if matches:
            return matches[0]
        else:
            raise ValueError(f"Attachment with ID {attachment_id} not existed")

    def remove_attachment_by_id(self, attachment_id: str):
        # Check if provided attachmend_id existed
        self.get_attachment_by_id(attachment_id)

        self._attachments = [a for a in self._attachments if a.id != attachment_id]

    def remove_attachments(self, attachments: list[str]) -> None:
        """
        attachments: list[attachment_id]
        """
        # Check if provided attachmend_id existed
        for attachment_id in attachments:
            self.get_attachment_by_id(attachment_id)

        self._attachments = [a for a in self._attachments if a.id not in attachments]

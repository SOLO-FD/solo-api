from typing import Annotated
from fastapi import Depends
from .session import SessionDep
from api.service import (
    ProjectService,
    ProjectTagService,
    TagService,
)


def get_project_service(session: SessionDep):
    return ProjectService(session)


ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]


def get_project_tag_service(session: SessionDep):
    return ProjectTagService(session)


ProjectTagServiceDep = Annotated[ProjectTagService, Depends(get_project_tag_service)]


def get_tag_service(session: SessionDep):
    return TagService(session)


TagServiceDep = Annotated[TagService, Depends(get_tag_service)]

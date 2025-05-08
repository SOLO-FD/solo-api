from fastapi import APIRouter, HTTPException

from api.dependencies import (
    ProjectServiceDep,
    CurrentAccountIdDep,
)
from api.dto import (
    ProjectCreateDTO,
    ProjectPublicDTO,
    ProjectUpdateDTO,
)

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("/", response_model=ProjectPublicDTO)
async def create_project(
    project: ProjectCreateDTO,
    service: ProjectServiceDep,
    account_id: CurrentAccountIdDep,
):
    return await service.create(account_id, project)


@router.get("/", response_model=list[ProjectPublicDTO])
async def read_projects(
    service: ProjectServiceDep,
    account_id: CurrentAccountIdDep,
):
    return await service.list_by_owner_id(account_id)


@router.get("/{project_id}", response_model=ProjectPublicDTO)
async def read_project(
    project_id: str,
    service: ProjectServiceDep,
    account_id: CurrentAccountIdDep,
):
    try:
        project = await service.get_by_id(account_id, project_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectPublicDTO)
async def update_project(
    project_id: str,
    project: ProjectUpdateDTO,
    service: ProjectServiceDep,
    account_id: CurrentAccountIdDep,
):
    try:
        project = await service.update(account_id, project_id, project)
    except ValueError:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    service: ProjectServiceDep,
    account_id: CurrentAccountIdDep,
):
    try:
        await service.delete_by_id(account_id, project_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Project not found")


@router.delete("/{project_id}/attachments/{attachment_id}", status_code=204)
async def remove_attachment(
    project_id: str,
    attachment_id: str,
    service: ProjectServiceDep,
    account_id: CurrentAccountIdDep,
):
    try:
        await service.remove_attachment_by_id(account_id, project_id, attachment_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Attachment not found")

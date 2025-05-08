from fastapi import APIRouter, HTTPException

from api.dependencies import (
    ProjectTagServiceDep,
    CurrentAccountIdDep,
)
from api.dto import (
    ProjectTagPublicDTO,
    ProjectPublicDTO,
)

router = APIRouter(
    tags=["project-tag"],
)


@router.put(
    "/projects/{project_id}/tags/{tag_id}", response_model=list[ProjectTagPublicDTO]
)
async def add_tag_to_project(
    project_id: str,
    tag_id: str,
    service: ProjectTagServiceDep,
    account_id: CurrentAccountIdDep,
):
    return await service.add_tag_by_id(account_id, project_id, tag_id)


@router.get("/projects/{project_id}/tags/", response_model=list[ProjectTagPublicDTO])
async def list_tags_by_project_id(
    project_id: str,
    service: ProjectTagServiceDep,
    account_id: CurrentAccountIdDep,
):
    return await service.list_by_project_id(account_id, project_id)


@router.get("/tags/{tag_id}/projects/", response_model=list[ProjectPublicDTO])
async def list_projects_by_tag_id(
    tag_id: str,
    service: ProjectTagServiceDep,
    account_id: CurrentAccountIdDep,
):
    return await service.list_by_tag_id(account_id, tag_id)


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    service: ProjectTagServiceDep,
    account_id: CurrentAccountIdDep,
):
    try:
        await service.delete_by_id(account_id, project_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Project not found")


@router.delete("/projects/{project_id}/tags/{tag_id}", status_code=204)
async def remove_tag_from_project(
    project_id: str,
    tag_id: str,
    service: ProjectTagServiceDep,
    account_id: CurrentAccountIdDep,
):
    try:
        await service.remove_tag_by_id(account_id, project_id, tag_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Given Tag not in given Project")

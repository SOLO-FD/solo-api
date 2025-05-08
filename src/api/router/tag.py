from fastapi import APIRouter, HTTPException

from api.dependencies import (
    TagServiceDep,
    CurrentAccountIdDep,
)
from api.dto import (
    TagCreateDTO,
    TagPublicDTO,
    TagUpdateDTO,
)

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
)


@router.post("/", response_model=TagPublicDTO)
async def create_tag(
    tag: TagCreateDTO,
    service: TagServiceDep,
    account_id: CurrentAccountIdDep,
):
    return await service.create(account_id, tag)


@router.get("/", response_model=list[TagPublicDTO])
async def read_tags(
    service: TagServiceDep,
    account_id: CurrentAccountIdDep,
):
    return await service.list_by_owner_id(account_id)


@router.get("/{tag_id}", response_model=TagPublicDTO)
async def read_tag(
    tag_id: str,
    service: TagServiceDep,
    account_id: CurrentAccountIdDep,
):
    try:
        tag = await service.get_by_id(account_id, tag_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.patch("/{tag_id}", response_model=TagPublicDTO)
async def update_tag(
    tag_id: str,
    tag: TagUpdateDTO,
    service: TagServiceDep,
    account_id: CurrentAccountIdDep,
):
    try:
        tag = await service.update(account_id, tag_id, tag)
    except ValueError:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: str,
    service: TagServiceDep,
    account_id: CurrentAccountIdDep,
):
    try:
        await service.delete_by_id(account_id, tag_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Tag not found")

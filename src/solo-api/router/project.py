from fastapi import APIRouter, Query
from sqlalchemy import select
from typing import Annotated

from ..models.project import Project
from ..dependencies.session import SessionDep

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("/projects/")
def create_project(project: Project, session: SessionDep) -> Project:
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("/projects/")
def read_projects(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Project]:
    projects = session.execute(select(Project).offset(offset).limit(limit)).all()
    return projects

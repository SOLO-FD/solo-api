from fastapi import APIRouter
from sqlmodel import Session, select

from ..model.project import project
from ..database import engine

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("/projects/")
def create_project(project: project):
    with Session(engine) as session:
        session.add(project)
        session.commit()
        session.refresh(project)
        return project


@router.get("/projects/")
def read_projects():
    with Session(engine) as session:
        projects = session.exec(select(project)).all()
        return projects

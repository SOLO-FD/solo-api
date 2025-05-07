from fastapi import APIRouter


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

# @router.post("/", response_model=ProjectPublicDTO)
# async def create_project(project: ProjectCreateDTO, session: SessionDep):
#     db_project = Project.model_validate(project)

#     repo = ProjectRepo(session)
#     return await repo.create(project_domain)


# @router.get("/", response_model=list[ProjectPublicDTO])
# async def read_projectes(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ):
#     projectes = session.exec(select(Project).offset(offset).limit(limit)).all()
#     return projectes


# @router.get("/{project_id}", response_model=ProjectPublicDTO)
# async def read_project(project_id: int, session: SessionDep):
#     project = session.get(Project, project_id)
#     if not project:
#         raise HTTPException(status_code=404, detail="Project not found")
#     return project


# @router.patch("/{project_id}", response_model=ProjectPublicDTO)
# async def update_project(project_id: int, project: ProjectUpdateDTO, session: SessionDep):
#     project_db = session.get(Project, project_id)
#     if not project_db:
#         raise HTTPException(status_code=404, detail="Project not found")
#     project_data = project.model_dump(exclude_unset=True)
#     project_db.sqlmodel_update(project_data)
#     session.add(project_db)
#     session.commit()
#     session.refresh(project_db)
#     return project_db


# @router.delete("/{project_id}")
# async def delete_project(project_id: int, session: SessionDep):
#     project = session.get(Project, project_id)
#     if not project:
#         raise HTTPException(status_code=404, detail="Project not found")
#     session.delete(project)
#     session.commit()
#     return {"ok": True}

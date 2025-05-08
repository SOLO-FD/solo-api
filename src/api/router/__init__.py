from .project import router as project_router
from .tag import router as tag_router
from .project_tag import router as project_tag_router

routers = [
    project_router,
    tag_router,
    project_tag_router,
]

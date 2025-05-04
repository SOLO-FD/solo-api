from fastapi import FastAPI

from .router import routers

app = FastAPI()

# Adding routers to app
for r in routers:
    app.include_router(r, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "SOLO API Endpoints is health!"}

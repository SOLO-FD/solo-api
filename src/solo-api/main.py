from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import create_db_and_tables
from .router import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database and tables
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Adding routers to app
for r in routers:
    app.include_router(r)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

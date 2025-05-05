from typing import Annotated
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends
from typing import AsyncGenerator

from .setting import SettingDep


# Dependency function that creates the session on-demand
async def get_async_session(
    settings: SettingDep,
) -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        settings.db_url,
        echo=True,
        connect_args={"check_same_thread": False}
        if settings.db_url.startswith("sqlite")
        else {},
    )

    # Only apply PRAGMA if using SQLite
    if settings.db_url.startswith("sqlite"):

        @event.listens_for(engine.sync_engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session


# Annotated alias for reuse
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

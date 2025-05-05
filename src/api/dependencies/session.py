from typing import Annotated
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
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session


# Annotated alias for reuse
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

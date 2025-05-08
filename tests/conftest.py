import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import event
import tempfile

from api.database import Base
from api.main import app
from api.dependencies import get_async_session
from api.utils import generate_id


@pytest.fixture(name="session", scope="function")
async def session_fixture():
    # Create a truly persistent temp file path
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    db_url = f"sqlite+aiosqlite:///{path}"
    engine = create_async_engine(
        db_url,
        # echo=True,
        connect_args={"check_same_thread": False},
    )
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    # Enable PRAGMA foreign_keys for SQLite
    @event.listens_for(engine.sync_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Provide a clean session for the test
    async with async_session_maker() as session:
        yield session

    # Clean up temp file manually
    os.remove(path)


@pytest.fixture(name="client", scope="function")
def client_fixture(session):
    def get_async_session_override():
        return session

    app.dependency_overrides[get_async_session] = get_async_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="default_account_id", scope="function")
def default_account_id():
    return generate_id()

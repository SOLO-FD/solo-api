import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.api.database import Base
import tempfile

from src.api.main import app
from src.api.dependencies import get_async_session


@pytest.fixture(name="session", scope="function")
async def session_fixture():
    # Create a temporary file-based SQLite database
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        db_url = f"sqlite+aiosqlite:///{tmp.name}"
        engine = create_async_engine(db_url, connect_args={"check_same_thread": False})
        async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Provide a clean session for the test
        async with async_session_maker() as session:
            yield session

        # Tables will be dropped automatically when temp file is deleted


@pytest.fixture(name="client", scope="function")
def client_fixture(session):
    def get_async_session_override():
        return session

    app.dependency_overrides[get_async_session] = get_async_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

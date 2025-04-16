import asyncio
import pickle
from unittest.mock import patch, AsyncMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from src.database.models import Base, User
from src.database.db import get_db
from src.services.auth import Hash
from src.utils.tokens import create_access_token


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

test_user = {
    "username": "deadpool",
    "email": "deadpool@example.com",
    "password": "12345678",
    "role": "user",
    
}

test_admin_user = User(
    username="deadpool",
    email="deadpool@example.com",
    hashed_password=Hash().get_password_hash("12345678"), 
    role="admin",
   
)


@pytest.fixture(scope="module", autouse=True)
def init_models_wrap():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal() as session:
            hash_password = Hash().get_password_hash(test_user["password"])
            current_user = User(
                username=test_user["username"],
                email=test_user["email"],
                hashed_password=hash_password,
                is_verified=True,
                avatar="https://twitter.com/gravatar",
            )
            session.add(current_user)
            await session.commit()

    asyncio.run(init_models())


@pytest.fixture(scope="module")
def client():
    async def override_get_db():
        async with TestingSessionLocal() as session:
            try:
                yield session
            except Exception as err:
                await session.rollback()
                raise
        
    
    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def get_token():
    token = await create_access_token(data={"sub": test_user["username"]})
    return token


# @pytest.fixture(scope="module")
# def mock_redis():
#     with patch("src.core.redis_client.redis.from_url") as mock_from_url:
#         redis_instance = AsyncMock()
#         redis_instance.get.return_value = None
#         redis_instance.set.return_value = True
#         mock_from_url.return_value = redis_instance
#         yield redis_instance


@pytest.fixture(autouse=True)
def mock_redis_client():
    patcher = patch("src.services.auth.redis_client", new_callable=AsyncMock)
    mock = patcher.start()

    # емуляція методів
    mock.hgetall.return_value = {}
    mock.hset.return_value = True
    mock.expire.return_value = True
    mock.delete.return_value = True

    yield mock
    patcher.stop()

import asyncio
import pickle
from unittest.mock import patch, AsyncMock
import time
from sqlalchemy.future import select

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from src.database.models import Base, User, UserRole
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


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db

test_user = {
    "username": "deadpool",
    "email": "deadpool@example.com",
    "password": "12345678",
    "role": "user",
    
}


@pytest_asyncio.fixture(scope="module", autouse=True)
async def init_models_wrap():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        # Створення звичайного користувача
        hash_password = Hash().get_password_hash(test_user["password"])
        current_user = User(
            username=test_user["username"],
            email=test_user["email"],
            hashed_password=hash_password,
            is_verified=True,
            avatar="https://twitter.com/gravatar",
        )
        session.add(current_user)

        # Створення адміністратора
        hash_admin_pass = Hash().get_password_hash("adminpassword")
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hash_admin_pass,
            is_verified=True,
            avatar="https://twitter.com/adminavatar",
            role=UserRole.ADMIN,  
        )
        session.add(admin_user)

        await session.commit()
        await session.refresh(current_user)
        await session.refresh(admin_user)


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


@pytest_asyncio.fixture()
async def get_token_admin(init_models_wrap):
    token = await create_access_token(data={"sub": "admin@example.com"})
    return token

@pytest.fixture(autouse=True)
def mock_redis_client():
    targets = [
        "src.services.auth.redis_client",
        "src.api.users.redis_client",
    ]
    patchers = [patch(target, new_callable=AsyncMock) for target in targets]
    mocks = [p.start() for p in patchers]

    store = {}

    async def fake_get(key):
        data = store.get(key)
        if data:
            value, expires_at = data
            if expires_at > time.time():
                return str(value)
            else:
                del store[key]
        return None

    async def fake_set(key, value, ex=None):
        expires_at = time.time() + ex if ex else float("inf")
        store[key] = (int(value), expires_at)
        return True

    async def fake_incr(key):
        value, expires_at = store.get(key, (0, float("inf")))
        value += 1
        store[key] = (value, expires_at)
        return value

    async def fake_delete(key):
        return store.pop(key, None)

    for mock in mocks:
        mock.get.side_effect = fake_get
        mock.set.side_effect = fake_set
        mock.incr.side_effect = fake_incr
        mock.delete.side_effect = fake_delete

        # залишаєш старі заглушки, якщо десь ще використовуються
        mock.hgetall.return_value = {}
        mock.hset.return_value = True
        mock.expire.return_value = True

    yield mocks[0]

    for p in patchers:
        p.stop()

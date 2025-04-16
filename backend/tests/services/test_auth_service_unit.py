
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from src.services.auth import get_current_user, get_current_admin_user
from src.schemas import User as UserSchema
from src.database.models import UserRole, User
from jose import JWTError


@pytest.fixture
def valid_payload():
    return {"sub": "testuser"}


@pytest.fixture
def user_schema():
    return UserSchema(
        id=1,
        username="testuser",
        email="test@example.com",
        avatar="avatar.png",
        role=UserRole.USER,
    )


@pytest.fixture
def admin_user_schema():
    return UserSchema(
        id=2,
        username="admin",
        email="admin@example.com",
        avatar="",
        role=UserRole.ADMIN,
    )


# Тест для перевірки ORM моделі User:
@pytest.mark.asyncio
async def test_get_current_user_from_cache(valid_payload, user_schema):
    with patch("src.services.auth.jwt.decode", return_value=valid_payload), patch(
        "src.services.auth.redis_client.hgetall",
        new=AsyncMock(
            return_value={
                "id": "1",
                "username": "testuser",
                "email": "test@example.com",
                "avatar": "avatar.png",
                "role": "user",
            }
        ),
    ):
        db_mock = MagicMock()
        # Створюємо мок для db.query(User).get(), щоб він повертав реальний екземпляр User
        db_mock.query(User).get.return_value = User(
            id=1,
            username="testuser",
            email="test@example.com",
            avatar="avatar.png",
            role=UserRole.USER,
        )

        result = await get_current_user(token="token", db=db_mock)

        # Перевіряємо, що результат є ORM моделлю User
        assert isinstance(result, User)

        # Перевіряємо значення
        assert result.username == "testuser"
        assert result.email == "test@example.com"
        assert result.role == UserRole.USER


@pytest.mark.asyncio
async def test_get_current_user_from_db(valid_payload, user_schema):
    with patch("src.services.auth.jwt.decode", return_value=valid_payload), patch(
        "src.services.auth.redis_client.hgetall", new=AsyncMock(return_value={})
    ), patch(
        "src.services.auth.UserService.get_user_by_username",
        new=AsyncMock(return_value=user_schema),
    ), patch(
        "src.services.auth.redis_client.hset", new=AsyncMock()
    ), patch(
        "src.services.auth.redis_client.expire", new=AsyncMock()
    ):
        db_mock = MagicMock()
        db_mock.return_value = db_mock
        result = await get_current_user(token="token", db=db_mock)
        assert isinstance(result, UserSchema)
        assert result.username == "testuser"


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    with patch("src.services.auth.jwt.decode", side_effect=JWTError("Invalid token")):
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token="invalid", db=MagicMock())
        assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_admin_user_success(admin_user_schema):
    result = get_current_admin_user(admin_user_schema)
    assert result.role == UserRole.ADMIN


@pytest.mark.asyncio
async def test_get_current_admin_user_forbidden(user_schema):
    with pytest.raises(HTTPException) as exc_info:
        get_current_admin_user(user_schema)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Недостатньо прав доступу"

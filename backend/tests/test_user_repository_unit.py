import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.repository.users import UserRepository
from src.schemas import UserCreate
from src.database.models import UserRole


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def user_repository(mock_session):
    return UserRepository(mock_session)


@pytest.fixture
def test_user():
    return User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        hashed_password="Hashedpassword1!",
    )


@pytest.mark.asyncio
async def test_get_user_by_id(user_repository, mock_session, test_user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = test_user
    mock_session.execute.return_value = mock_result

    # Call method
    user = await user_repository.get_user_by_id(user_id=1)

    # Assertions
    assert user is not None
    assert user.id == 1
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_email(user_repository, mock_session, test_user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = test_user
    mock_session.execute.return_value = mock_result

    # Call method
    user = await user_repository.get_user_by_email(email="testuser@example.com")

    # Assertions
    assert user is not None
    assert user.email == "testuser@example.com"
    assert user.username == "testuser"
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_by_username(user_repository, mock_session, test_user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = test_user
    mock_session.execute.return_value = mock_result

    # Call method
    user = await user_repository.get_user_by_username(username="testuser")

    # Assertions
    assert user is not None
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_create_user(user_repository, mock_session):
    # Setup
    user_data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="Hashedpassword1!",
    )

    # Setup mock
    def add_side_effect(obj):
        obj.id = 2
        obj.role = "user"
        return None

    mock_session.add.side_effect = add_side_effect
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Call the actual method — тепер передаємо avatar та role
    result = await user_repository.create_user(
        user_data, avatar="https://some.url/avatar.png", role=UserRole.USER
    )

    # Assertions
    assert isinstance(result, User)
    assert result.username == "newuser"
    assert result.email == "newuser@example.com"
    mock_session.add.assert_called_once_with(result)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(result)

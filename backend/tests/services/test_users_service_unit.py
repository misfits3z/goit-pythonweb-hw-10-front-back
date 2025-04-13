import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.schemas import UserCreate
from src.database.models import User, UserRole
from src.services.users import UserService


@pytest.fixture
def user_create_data():
    return UserCreate(
        username="tonystark", email="tony@starkindustries.com", password="ironman3000"
    )


@pytest.fixture
def fake_user():
    return User(
        id=1,
        username="tonystark",
        email="tony@starkindustries.com",
        role=UserRole.USER,
        is_verified=False,
    )


@pytest.fixture
def service():
    mock_repo = MagicMock()
    return UserService(db=mock_repo)


@pytest.mark.asyncio
@patch("src.services.users.generate_verification_token", new_callable=AsyncMock)
@patch("src.services.users.Gravatar")
@patch("src.services.users.aiosmtplib.send", new_callable=AsyncMock)
async def test_create_user(
    mock_send, mock_gravatar, mock_token, service, user_create_data, fake_user
):
    service.repository.create_user = AsyncMock(return_value=fake_user)
    mock_token.return_value = "mocked_token"
    mock_gravatar.return_value.get_image.return_value = "avatar_url"

    user = await service.create_user(user_create_data)

    assert user == fake_user
    service.repository.create_user.assert_awaited_once()
    mock_token.assert_awaited_once_with("tony@starkindustries.com")
    mock_send.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_id(service, fake_user):
    service.repository.get_user_by_id = AsyncMock(return_value=fake_user)

    user = await service.get_user_by_id(1)

    assert user == fake_user
    service.repository.get_user_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_user_by_username(service, fake_user):
    service.repository.get_user_by_username = AsyncMock(return_value=fake_user)

    user = await service.get_user_by_username("tonystark")

    assert user == fake_user
    service.repository.get_user_by_username.assert_awaited_once_with("tonystark")


@pytest.mark.asyncio
async def test_get_user_by_email(service, fake_user):
    service.repository.get_user_by_email = AsyncMock(return_value=fake_user)

    user = await service.get_user_by_email("tony@starkindustries.com")

    assert user == fake_user
    service.repository.get_user_by_email.assert_awaited_once_with(
        "tony@starkindustries.com"
    )


@pytest.mark.asyncio
@patch("src.services.users.aiosmtplib.send", new_callable=AsyncMock)
async def test_send_verification_email(mock_send, service):
    await service.send_verification_email("tony@starkindustries.com", "token123")
    mock_send.assert_awaited_once()


@pytest.mark.asyncio
@patch("src.services.users.aiosmtplib.send", new_callable=AsyncMock)
async def test_send_password_reset_email(mock_send, service):
    await service.send_password_reset_email("tony@starkindustries.com", "token456")
    mock_send.assert_awaited_once()


@pytest.mark.asyncio
@patch("src.services.users.aiosmtplib.send", new_callable=AsyncMock)
async def test_send_verification_email_failure(mock_send, service):
    mock_send.side_effect = Exception("SMTP error")
    await service.send_verification_email("tony@starkindustries.com", "token123")
    mock_send.assert_awaited_once()


@pytest.mark.asyncio
@patch("src.services.users.aiosmtplib.send", new_callable=AsyncMock)
async def test_send_password_reset_email_failure(mock_send, service):
    mock_send.side_effect = Exception("SMTP error")
    await service.send_password_reset_email("tony@starkindustries.com", "token456")
    mock_send.assert_awaited_once()

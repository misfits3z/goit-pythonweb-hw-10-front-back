import pytest
from unittest.mock import AsyncMock, MagicMock

from src.services.contacts import ContactService
from src.schemas import ContactCreate
from src.database.models import User
from datetime import date

@pytest.fixture
def mock_user():
    return User(id=1, username="vika")


@pytest.fixture
def mock_contact():
    return {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "123456789",
    }


@pytest.fixture
def contact_data():
    return ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone_number="123456789",
        birth_date=date(1990, 1, 1),
    )


@pytest.fixture
def service():
    mock_repo = AsyncMock()
    service = ContactService(db=MagicMock())
    service.repository = mock_repo
    return service


@pytest.mark.asyncio
async def test_create_contact(service, contact_data, mock_user, mock_contact):
    service.repository.create_contact.return_value = mock_contact

    result = await service.create_contact(contact_data, mock_user)

    service.repository.create_contact.assert_awaited_once_with(contact_data, mock_user)
    assert result == mock_contact


@pytest.mark.asyncio
async def test_get_contacts(service, mock_user):
    expected = [{"id": 1}, {"id": 2}]
    service.repository.get_contacts.return_value = expected

    result = await service.get_contacts(skip=0, limit=10, user=mock_user)

    service.repository.get_contacts.assert_awaited_once_with(0, 10, mock_user)
    assert result == expected


@pytest.mark.asyncio
async def test_get_contact(service, mock_user):
    expected = {"id": 1}
    service.repository.get_contact_by_id.return_value = expected

    result = await service.get_contact(contact_id=1, user=mock_user)

    service.repository.get_contact_by_id.assert_awaited_once_with(1, mock_user)
    assert result == expected


@pytest.mark.asyncio
async def test_update_contact(service, contact_data, mock_user):
    updated_contact = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone_number": "123456789",
        "birth_date": date(1990, 1, 1),
    }
    service.repository.update_contact.return_value = updated_contact

    result = await service.update_contact(1, contact_data, mock_user)

    service.repository.update_contact.assert_awaited_once_with(
        1, contact_data, mock_user
    )
    assert result == updated_contact


@pytest.mark.asyncio
async def test_remove_contact(service, mock_user):
    deleted_contact = {"id": 1}
    service.repository.remove_contact.return_value = deleted_contact

    result = await service.remove_contact(1, mock_user)

    service.repository.remove_contact.assert_awaited_once_with(1, mock_user)
    assert result == deleted_contact

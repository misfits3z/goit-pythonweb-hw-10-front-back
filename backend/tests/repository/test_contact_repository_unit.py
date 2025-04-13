import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from datetime import date

from src.database.models import Contact, User
from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def contact_repository(mock_session):
    return ContactRepository(mock_session)


@pytest.fixture
def user():
    return User(id=1, username="testuser", email="testuser@example.com")


@pytest.mark.asyncio
async def test_get_contacts(contact_repository, mock_session, user):
    # Створюємо фейковий результат SELECT
    contact_instance = Contact(
        id=1,
        first_name="Bob",
        last_name="Thomson",
        email="bobthomson@example.com",
        user_id=user.id,
    )

    # Створюємо мок для `scalars().all()`
    mock_result = MagicMock(spec=Result)
    mock_result.scalars.return_value.all.return_value = [contact_instance]

    # Підмінюємо execute
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Викликаємо метод
    contacts = await contact_repository.get_contacts(skip=0, limit=10, user=user)

    # Перевірки
    assert isinstance(contacts, list)
    assert len(contacts) == 1
    assert contacts[0].first_name == "Bob"
    assert contacts[0].email == "bobthomson@example.com"
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_contact_by_id(contact_repository, mock_session, user):
    contact_instance = Contact(
        id=1,
        first_name="Bob",
        last_name="Thomson",
        email="bobthomson@example.com",
        user_id=user.id,
    )

    # Створюємо мок для `scalars().all()`
    mock_result = MagicMock(spec=Result)
    mock_result.scalar_one_or_none.return_value = contact_instance

    # Підмінюємо execute
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Викликаємо метод
    contact = await contact_repository.get_contact_by_id(contact_id=1, user=user)

    # Перевірки
    assert contact is not None
    assert contact.first_name == "Bob"
    assert contact.email == "bobthomson@example.com"
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_create_contact(contact_repository, mock_session, user):
    contact_test = ContactCreate(
        first_name="Bob",
        last_name="Thomson",
        email="bobthomson@example.com",
        phone_number="18689200055",
        birth_date=date(1995, 5, 15),
    )

    created_contact = Contact(
        id=1,
        first_name="Bob",
        last_name="Thomson",
        email="bobthomson@example.com",
        phone_number="18689200055",
        birth_date=date(1995, 5, 15),
        user_id=user.id,
    )

    mock_session.add = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    contact_repository.get_contact_by_id = AsyncMock(return_value=created_contact)

    # Викликаємо метод
    res = await contact_repository.create_contact(contact_test, user=user)
    

    assert res is not None
    assert res.first_name == "Bob"
    assert res.email == "bobthomson@example.com"
    assert res.user_id == user.id
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_contact(contact_repository, mock_session, user):
    contact_data = ContactCreate(
        first_name="Mark",
        last_name="Thomson",
        email="markthomson@example.com",
        phone_number="18689200033",
        birth_date=date(1991, 5, 20),
    )
    existing_contact = Contact(
        id=1,
        first_name="Bob",
        last_name="Thomson",
        email="bobthomson@example.com",
        phone_number="18689200055",
        birth_date=date(1995, 5, 15),
        user_id=user.id
    )
    
    contact_repository.get_contact_by_id = AsyncMock(return_value=existing_contact)

    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    result = await contact_repository.update_contact(
        contact_id=1, body=contact_data, user=user
    )

    
    assert result is not None
    assert result.first_name == "Mark"
    assert result.email == "markthomson@example.com"
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(existing_contact)


@pytest.mark.asyncio
async def test_remove_contact(contact_repository, mock_session, user):
    # Setup
    existing_contact = Contact(
        id=1,
        first_name="Bob",
        last_name="Thomson",
        email="bobthomson@example.com",
        user_id=user.id,
    )
    contact_repository.get_contact_by_id = AsyncMock(return_value=existing_contact)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    # Call method
    result = await contact_repository.remove_contact(contact_id=1, user=user)

    # Assertions
    assert result is not None
    assert result.first_name == "Bob"
    mock_session.delete.assert_awaited_once_with(existing_contact)
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_contacts_by_ids(contact_repository, mock_session, user):
    contact1 = Contact(
        id=1,
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        user_id=user.id,
    )

    contact2 = Contact(
        id=2,
        first_name="Bob",
        last_name="Johnson",
        email="bob@example.com",
        user_id=user.id,
    )

    mock_result = MagicMock(spec=Result)
    mock_result.scalars.return_value.all.return_value = [contact1, contact2]
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await contact_repository.get_contacts_by_ids([1, 2], user=user)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
    mock_session.execute.assert_called_once()

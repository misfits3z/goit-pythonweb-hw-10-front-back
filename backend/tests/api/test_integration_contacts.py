import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from src.utils.tokens import create_access_token
from src.database.models import Contact
from tests.api.conftest import TestingSessionLocal
from datetime import date, timedelta


# @pytest.mark.asyncio
def test_create_contact(client, get_token):
    access_token = get_token
    headers = {"Authorization": f"Bearer {access_token}"}

    contact_data = {
        "first_name": "Bruce",
        "last_name": "Wayne",
        "email": "batman@example.com",
        "phone_number": "1234567890",
        "birth_date": "1980-01-01",
        "note": "The Dark Knight",
    }

    response =  client.post("/api/contacts", json=contact_data, headers=headers)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["first_name"] == contact_data["first_name"]
    assert data["last_name"] == contact_data["last_name"]
    assert data["email"] == contact_data["email"]


def test_read_contacts(client, get_token):
    token = get_token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("api/contacts/", headers=headers)
    assert response.status_code == 200


def test_get_contact(client, get_token):
    response = client.get(
        "/api/contacts/1", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "Bruce"
    assert "id" in data


def test_get_contact_not_found(client, get_token):
    response = client.get(
        "/api/contacts/2", headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Contact not found"


@pytest.mark.asyncio
async def test_update_contact(client, get_token):
    token = get_token
    headers = {"Authorization": f"Bearer {token}"}
    contact_data = {
        "first_name": "Natasha",
        "last_name": "Romanoff",
        "email": "blackwidow@shield.org",
        "phone_number": "123-000-0001",
        "birth_date": "1984-11-22",
    }

    updated_data = {
        "first_name": "Nat",
        "last_name": "Romanoff",
        "email": "natasha@avengers.com",
        "phone_number": "999-999-9999",
        "birth_date": "1984-11-22",
    }

    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_response = await ac.post(
            "/api/contacts/", json=contact_data, headers=headers
        )
        print("Create response status:", create_response.status_code)
        print("Create response json:", create_response.json())
        contact_id = create_response.json()["id"]

        response = await ac.put(
            f"/api/contacts/{contact_id}", json=updated_data, headers=headers
        )
    assert response.status_code == 200
    assert response.json()["email"] == "natasha@avengers.com"
    assert response.json()["first_name"] == "Nat"


@pytest.mark.asyncio
async def test_delete_contact(client, get_token):
    token = get_token
    headers = {"Authorization": f"Bearer {token}"}
    contact_data = {
        "first_name": "Loki",
        "last_name": "Odinson",
        "email": "loki@asgard.com",
        "phone_number": "666-666-6666",
        "birth_date": "1000-01-01",
    }
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_response = await ac.post(
            "/api/contacts/", json=contact_data, headers=headers
        )
        contact_id = create_response.json()["id"]

        response = await ac.delete(f"/api/contacts/{contact_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "loki@asgard.com"


@pytest.mark.asyncio
async def test_search_contacts(client, get_token):
    token = get_token

    # Створюємо тестові контакти
    contact_data = [
        Contact(
            first_name="Bruce",
            last_name="Wayne",
            email="bruce@wayne.com",
            phone_number="123456789",
            birth_date=date(1990, 5, 15),
            user_id=1,
        ),
        Contact(
            first_name="Clark",
            last_name="Kent",
            email="clark@dailyplanet.com",
            phone_number="987654321",
            birth_date=date(1988, 6, 20),
            user_id=1,
        ),
    ]

    async with TestingSessionLocal() as session:
        session.add_all(contact_data)
        await session.commit()

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/contacts/search/?first_name=bruce",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("Bruce" in c["first_name"] for c in data)


@pytest.mark.asyncio
async def test_get_upcoming_birthdays(client, get_token):
    token = get_token
    today = date.today()
    upcoming = today + timedelta(days=5)

    contact = Contact(
        first_name="Birthday",
        last_name="Person",
        email="birthday@example.com",
        phone_number="111222333",
        birth_date=upcoming,
        user_id=1,
    )

    async with TestingSessionLocal() as session:
        session.add(contact)
        await session.commit()
        
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/contacts/birthdays/?days=7",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert any("birthday@example.com" in c["email"] for c in result)

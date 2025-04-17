import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from src.utils.tokens import create_access_token


# def test_create_contact(client, get_token):
#     token = get_token  # Отримуємо правильний токен
#     contact_data = {
#         "first_name": "Bruce",
#         "last_name": "Wayne",
#         "email": "batman@example.com",
#         "phone_number": "1234567890",
#         "birth_date": "1980-01-01",
#         "note": "The Dark Knight",
#     }

#     response = client.post(
#         "/api/contacts", json=contact_data, headers={"Authorization": f"Bearer {token}"}
#     )

#     assert response.status_code == 200


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
            "/contacts/", json=contact_data, headers=headers
        )
        contact_id = create_response.json()["id"]

        response = await ac.put(
            f"/contacts/{contact_id}", json=updated_data, headers=headers
        )
    assert response.status_code == 200
    assert response.json()["email"] == "natasha@avengers.com"
    assert response.json()["first_name"] == "Nat"


# @pytest.mark.asyncio
# async def test_delete_contact(client, get_token):
#     token = get_token
#     headers = {"Authorization": f"Bearer {token}"}
#     contact_data = {
#         "first_name": "Loki",
#         "last_name": "Odinson",
#         "email": "loki@asgard.com",
#         "phone": "666-666-6666",
#         "birthday": "1000-01-01",
#     }
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         create_response = await ac.post(
#             "/contacts/", json=contact_data, headers=headers
#         )
#         contact_id = create_response.json()["id"]

#         response = await ac.delete(f"/contacts/{contact_id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["email"] == "loki@asgard.com"

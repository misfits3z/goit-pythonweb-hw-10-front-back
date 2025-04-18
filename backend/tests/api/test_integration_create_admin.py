
from main import app
from fastapi import status
from httpx import AsyncClient, ASGITransport
import pytest



@pytest.mark.asyncio
async def test_create_admin_success(client, get_token_admin):
    
    new_admin_data = {
        "username": "newadmin",
        "email": "newadmin@example.com",
        "password": "securepassword123",
    }

    headers = {"Authorization": f"Bearer {get_token_admin}"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/create-admin", json=new_admin_data, headers=headers)

    # Перевірка
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == new_admin_data["username"]
    assert data["email"] == new_admin_data["email"]
    assert data["role"] == "admin"
    assert "id" in data
    

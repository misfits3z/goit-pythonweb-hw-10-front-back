import pytest
from httpx import AsyncClient, ASGITransport
from main import app




# @pytest.mark.asyncio
# async def test_create_admin_user(get_token_admin):
#     token =  get_token_admin 

#     payload = {
#         "username": "newadmin",
#         "email": "newadmin@example.com",
#         "password": "StrongPass123",
#     }

#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
#         response = await ac.post(
#             "/api/create-admin",
#             json=payload,
#             headers={"Authorization": f"Bearer {token}"},
#         )

#     assert response.status_code == 201
#     data = response.json()
#     assert data["email"] == payload["email"]
#     assert data["role"] == "admin"

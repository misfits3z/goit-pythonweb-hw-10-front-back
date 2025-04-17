import pytest
from fastapi import status
from src.schemas import User
from src.services.auth import Hash
from tests.api.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_get_current_user(client, get_token, mock_redis_client):
    """
    Test retrieving the current authenticated user's details.
    """
    headers = {"Authorization": f"Bearer {get_token}"}
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "username" in data
    assert "email" in data
    assert data["username"] == "deadpool"
    assert data["email"] == "deadpool@example.com"


@pytest.mark.asyncio
async def test_rate_limit(client, get_token):
    # Виконання більше 10 запитів
    for _ in range(10):
        response = client.get(
            "/api/users/me", headers={"Authorization": f"Bearer {get_token}"}
        )
        assert response.status_code == status.HTTP_200_OK

    # 11-й запит має отримати помилку 429
    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {get_token}"})
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.asyncio
async def test_update_avatar_for_admin(client, get_token_admin):
    # Запит на зміну аватара для адміністратора
    new_avatar = "https://new-avatar.com/avatar.png"
    response = client.patch(
        "/api/users/avatar",
        json={"new_avatar": new_avatar},
        headers={"Authorization": f"Bearer {get_token_admin}"},
    )

    # Перевірка статусу
    assert response.status_code == status.HTTP_200_OK

    # Перевірка аватара
    response_data = response.json()
    assert response_data["message"] == "Аватар оновлено"
    assert response_data["avatar"] == new_avatar


# @pytest.mark.asyncio
# async def test_update_avatar_for_non_admin(client, get_token):
#     # Запит на зміну аватара для користувача без прав адміністратора
#     new_avatar = "https://new-avatar.com/avatar.png"
#     response = client.patch(
#         "/api/users/avatar",
#         json={"new_avatar": new_avatar},
#         headers={"Authorization": f"Bearer {get_token}"},
#     )

#     # Перевірка статусу (403 — заборонено)
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     assert (
#         response.json()["detail"]
#         == "Тільки адміністратор може змінити аватар за замовчуванням"
#     )


# @pytest.mark.asyncio
# async def test_update_avatar_user_not_found(client, get_token_admin):
#     # Вимкнути або змінити дані користувача для тесту
#     async with TestingSessionLocal() as session:
#         await session.execute("DELETE FROM users WHERE username = 'admin'")

#     # Запит на зміну аватара для адміністратора, коли користувач відсутній
#     new_avatar = "https://new-avatar.com/avatar.png"
#     response = client.patch(
#         "/api/users/avatar",
#         json={"new_avatar": new_avatar},
#         headers={"Authorization": f"Bearer {get_token_admin}"},
#     )

#     # Перевірка статусу (404 — не знайдено)
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#     assert response.json()["detail"] == "Користувача не знайдено"

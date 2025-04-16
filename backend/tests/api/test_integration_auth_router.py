from unittest.mock import Mock

import pytest
from sqlalchemy import select

from src.database.models import User
from tests.api.conftest import TestingSessionLocal
from src.utils.tokens import generate_verification_token

import pytest


# Тест реєстрації користувача
@pytest.mark.asyncio
async def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data


# Тест логіну користувача
@pytest.mark.asyncio
async def test_login_user(client):
    response = client.post(
        "/auth/login", data={"username": "deadpool", "password": "12345678"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Перевірка refresh_token тільки якщо він присутній
    if "refresh_token" in data:
        assert isinstance(data["refresh_token"], str)


# Тест refresh токена
@pytest.mark.asyncio
async def test_refresh_token(client):
    from src.utils.tokens import create_refresh_token

    refresh_token = await create_refresh_token(data={"sub": "deadpool"})
    


    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["refresh_token"] == refresh_token
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_verify_email(client):
    token = await generate_verification_token("deadpool@example.com")

    response = client.get(f"auth/verify-email?token={token}")

    assert response.status_code == 200
    assert response.json()["message"] == "Email verified successfully"


@pytest.mark.asyncio
async def test_password_reset_email(client):
    response = client.post(
        "/auth/password-reset-email", json={"email": "deadpool@example.com"}
    )

    assert response.status_code == 200
    assert (
        response.json()["message"] == "Password reset instructions sent to your email"
    )

from src.utils.tokens import generate_password_reset_token


@pytest.mark.asyncio
async def test_password_reset_confirm(client):
    token =  generate_password_reset_token("deadpool@example.com")

    response = client.post(
        "/auth/password-reset-confirm",
        json={"token": token, "new_password": "newsecurepassword"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Password reset successfully"

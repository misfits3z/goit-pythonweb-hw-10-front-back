import pytest
from jose import jwt


from src.utils.tokens import (
    create_access_token,
    generate_verification_token,
    generate_password_reset_token,
    create_refresh_token,
)
from src.conf.config import config


@pytest.mark.asyncio
async def test_create_access_token():
    data = {"sub": "tony@starkindustries.com"}
    token = await create_access_token(data, expires_delta=3600)
    decoded = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])

    assert decoded["sub"] == data["sub"]
    assert "exp" in decoded


@pytest.mark.asyncio
async def test_generate_verification_token():
    email = "tony@starkindustries.com"
    token = await generate_verification_token(email)
    decoded = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])

    assert decoded["sub"] == email
    assert "exp" in decoded


def test_generate_password_reset_token():
    email = "tony@starkindustries.com"
    token = generate_password_reset_token(email)
    decoded = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])

    assert decoded["sub"] == email
    assert "exp" in decoded


@pytest.mark.asyncio
async def test_create_refresh_token():
    data = {"sub": "tony@starkindustries.com"}
    token = await create_refresh_token(data, expires_delta=7200)
    decoded = jwt.decode(
        token, config.JWT_SECRET_REFRESH, algorithms=[config.JWT_ALGORITHM]
    )

    assert decoded["sub"] == data["sub"]
    assert "exp" in decoded

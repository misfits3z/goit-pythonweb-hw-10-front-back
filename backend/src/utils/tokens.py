from datetime import datetime, timedelta, UTC
from jose import jwt
from src.conf.config import config
from typing import Optional


# define a function to generate a new access token
async def create_access_token(data: dict, expires_delta: Optional[int] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(UTC) + timedelta(seconds=config.JWT_EXPIRATION_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt


async def generate_verification_token(email: str):
    expiration = datetime.now(UTC) + timedelta(hours=24)  # 24 години на підтвердження
    payload = {"sub": email, "exp": expiration}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


# password_reset_token
def generate_password_reset_token(email: str) -> str:
    expire = datetime.now() + timedelta(minutes=30)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt


async def create_refresh_token(data: dict, expires_delta: Optional[int] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(UTC) + timedelta(
            seconds=config.JWT_REFRESH_EXPIRATION_SECONDS
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET_REFRESH, algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt

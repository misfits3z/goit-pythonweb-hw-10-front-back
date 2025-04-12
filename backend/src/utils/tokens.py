from datetime import datetime, timedelta, UTC
from jose import jwt
from src.conf.config import config
from typing import Optional


async def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """
    Generates a new access token for the given data.

    Args:
        data (dict): The data to include in the token payload.
        expires_delta (Optional[int], optional): The expiration time of the token in seconds. If not provided,
        the default expiration from config is used.

    Returns:
        str: The generated JWT access token.
    """
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


async def generate_verification_token(email: str) -> str:
    """
    Generates a verification token for email verification.

    Args:
        email (str): The email to be used for generating the token.

    Returns:
        str: The generated JWT verification token.
    """
    expiration = datetime.now(UTC) + timedelta(
        hours=24
    )  # 24 hours for email verification
    payload = {"sub": email, "exp": expiration}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def generate_password_reset_token(email: str) -> str:
    """
    Generates a password reset token with a 30-minute expiration.

    Args:
        email (str): The email to be used for generating the password reset token.

    Returns:
        str: The generated JWT password reset token.
    """
    expire = datetime.now() + timedelta(minutes=30)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt


async def create_refresh_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """
    Generates a new refresh token for the given data.

    Args:
        data (dict): The data to include in the refresh token payload.
        expires_delta (Optional[int], optional): The expiration time of the token in seconds. If not provided,
        the default expiration from config is used.

    Returns:
        str: The generated JWT refresh token.
    """
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


# # define a function to generate a new access token
# async def create_access_token(data: dict, expires_delta: Optional[int] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
#     else:
#         expire = datetime.now(UTC) + timedelta(seconds=config.JWT_EXPIRATION_SECONDS)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
#     )
#     return encoded_jwt


# async def generate_verification_token(email: str):
#     expiration = datetime.now(UTC) + timedelta(hours=24)  # 24 години на підтвердження
#     payload = {"sub": email, "exp": expiration}
#     return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


# # password_reset_token
# def generate_password_reset_token(email: str) -> str:
#     expire = datetime.now() + timedelta(minutes=30)
#     to_encode = {"sub": email, "exp": expire}
#     encoded_jwt = jwt.encode(
#         to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
#     )
#     return encoded_jwt


# async def create_refresh_token(data: dict, expires_delta: Optional[int] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
#     else:
#         expire = datetime.now(UTC) + timedelta(
#             seconds=config.JWT_REFRESH_EXPIRATION_SECONDS
#         )
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         to_encode, config.JWT_SECRET_REFRESH, algorithm=config.JWT_ALGORITHM
#     )
#     return encoded_jwt

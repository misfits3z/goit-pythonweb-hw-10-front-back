from datetime import datetime, timedelta, UTC
from jose import jwt
from src.conf.config import config


async def generate_verification_token(email: str):
    expiration = datetime.now(UTC) + timedelta(hours=24)  # 24 години на підтвердження
    payload = {"sub": email, "exp": expiration}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

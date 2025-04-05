from fastapi import APIRouter, Depends, HTTPException
from src.schemas import User
from src.services.auth import get_current_user
import redis.asyncio as redis
import os

router = APIRouter(prefix="/users", tags=["users"])


# Підключення до Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis = redis.from_url(REDIS_URL, decode_responses=True)  


async def rate_limit(user: User):
    """Обмеження 10 запитів за 60 секунд через Redis"""
    key = f"user:{user.id}:requests"
    current_count = await redis.get(key)

    if current_count is None:
        # створюємо ключ з TTL 60 секунд
        await redis.set(key, 1, ex=60)
    else:
        current_count = int(current_count)
        if current_count >= 10:
            raise HTTPException(status_code=429, detail="Too Many Requests.")
        await redis.incr(key)  # Збільшуємо лічильник запитів


@router.get("/me", response_model=User)
async def me(user: User = Depends(get_current_user)):
    await rate_limit(user)  # Обмеження запитів через Redis
    return user

from fastapi import APIRouter, Depends, HTTPException
from src.schemas import User
from src.services.auth import get_current_user
import redis.asyncio as redis
import os
from src.repository.users import UserRepository
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.database.models import UserRole
from src.core.redis_client import redis_client
from src.schemas import AvatarUpdateSchema

router = APIRouter(prefix="/users", tags=["users"])


# Підключення до Redis
# REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
# redis = redis.from_url(REDIS_URL, decode_responses=True)


async def rate_limit(user: User):
    # Обмеження 10 запитів за 60 секунд через Redis
    """
    Apply a rate limit of 10 requests per 60 seconds using Redis.

    Args:
        user (User): The current authenticated user.

    Raises:
        HTTPException: If the user exceeds the allowed request rate.
    """

    key = f"user:{user.id}:requests"
    current_count = await redis_client.get(key)

    if current_count is None:
        # створюємо ключ з TTL 60 секунд
        await redis_client.set(key, 1, ex=60)
    else:
        current_count = int(current_count)
        if current_count >= 10:
            raise HTTPException(status_code=429, detail="Too Many Requests.")
        await redis_client.incr(key)  # Збільшуємо лічильник запитів


@router.get("/me", response_model=User)
async def me(user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.

    Args:
        user (User): The currently authenticated user (injected via dependency).

    Returns:
        User: The authenticated user's data.

    Raises:
        HTTPException: If rate limiting threshold is exceeded.
    """
    await rate_limit(user)  # Обмеження запитів через Redis
    return user


@router.patch("/avatar", status_code=status.HTTP_200_OK)
async def update_avatar_for_admin(
    payload: AvatarUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update the default avatar for the admin user.

    Args:
        new_avatar (str): The new avatar URL or base64 string.
        current_user (User): The currently authenticated user.
        db (AsyncSession): Database session.

    Returns:
        dict: Message confirming the avatar update with the updated avatar value.

    Raises:
        HTTPException:
            - 403: If the user is not an admin.
            - 404: If the user could not be found in the database.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Тільки адміністратор може змінити аватар за замовчуванням",
        )

    new_avatar = payload.new_avatar

    repo = UserRepository(db)
    updated_user = await repo.update_avatar(current_user.id, new_avatar)

    if not updated_user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    return {"message": "Аватар оновлено", "avatar": updated_user.avatar}

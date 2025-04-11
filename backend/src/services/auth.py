
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.database.db import get_db
from src.conf.config import config
from src.services.users import UserService
from src.database.models import User, UserRole
from src.core.redis_client import redis_client
from src.schemas import User as UserSchema

class Hash:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT decode error: {e}")
        raise credentials_exception

    # Перевірка в Redis
    redis_key = f"user:{username}"
    cached_user = await redis_client.hgetall(redis_key)
    if cached_user:
        try:
            cached_user["id"] = int(cached_user["id"])
            cached_user["role"] = UserRole(cached_user["role"])
            return UserSchema(**cached_user)
        except Exception:
            await redis_client.delete(redis_key)

    # Якщо не знайдено — беремо з БД
    user_service = UserService(db)
    user: User = await user_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception

    user_schema = UserSchema.model_validate(user)

    await redis_client.hset(
        redis_key,
        mapping={
            "id": str(user_schema.id),
            "username": user_schema.username,
            "email": user_schema.email,
            "role": user_schema.role.value,
            "avatar": user_schema.avatar or "",
        },
    )
    await redis_client.expire(redis_key, 600)  # 10 хвилин кешу

    return user_schema


# Залежність для перевірки ролей

def get_current_admin_user(current_user: UserSchema = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Недостатньо прав доступу")
    return current_user

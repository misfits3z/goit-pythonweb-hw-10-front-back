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
    """
    A utility class for handling password hashing and verification.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain password against a hashed password.

        Args:
            plain_password (str): The plain password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Hashes a plain password.

        Args:
            password (str): The plain password to hash.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    Retrieves the current user from the OAuth2 token.

    Args:
        token (str): The OAuth2 token to verify and decode.
        db (Session): The database session for querying user data.

    Returns:
        User: The ORM object representing the authenticated user.

    Raises:
        HTTPException: If the credentials are invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        username_or_email: str = payload.get("sub")
        if not username_or_email:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT decode error: {e}")
        raise credentials_exception

    redis_key = f"user:{username_or_email}"

    # Try to get from Redis
    cached_user = await redis_client.hgetall(redis_key)
    if cached_user:
        try:
            user_id = int(cached_user["id"])
            user = db.query(User).get(user_id)
            if user:
                return user
        except Exception as e:
            print(f"Redis cache parse error: {e}")
            await redis_client.delete(redis_key)

    # Fallback to DB, check if it's username or email
    user_service = UserService(db)
    user: User = await user_service.get_user_by_username(username_or_email)
    if not user:
        user: User = await user_service.get_user_by_email(username_or_email)

    if not user:
        raise credentials_exception

    # Cache in Redis
    await redis_client.hset(
        redis_key,
        mapping={
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "avatar": user.avatar or "",
        },
    )
    await redis_client.expire(redis_key, 600)

    return user


# async def get_current_user(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
# ) -> User:
#     """
#     Retrieves the current user from the OAuth2 token.

#     Args:
#         token (str): The OAuth2 token to verify and decode.
#         db (Session): The database session for querying user data.

#     Returns:
#         User: The ORM object representing the authenticated user.

#     Raises:
#         HTTPException: If the credentials are invalid or expired.
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(
#             token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
#         )
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError as e:
#         print(f"JWT decode error: {e}")
#         raise credentials_exception

#     # Check in Redis cache
#     redis_key = f"user:{username}"
#     cached_user = await redis_client.hgetall(redis_key)
#     if cached_user:
#         try:
#             user_id = int(cached_user["id"])
#             user = db.query(User).get(user_id)
#             if user:
#                 return user
#         except Exception:
#             await redis_client.delete(redis_key)

#     # Fallback to DB
#     user_service = UserService(db)
#     user: User = await user_service.get_user_by_username(username)
#     if user is None:
#         raise credentials_exception

#     # Cache user data in Redis
#     await redis_client.hset(
#         redis_key,
#         mapping={
#             "id": str(user.id),
#             "username": user.username,
#             "email": user.email,
#             "role": user.role.value,
#             "avatar": user.avatar or "",
#         },
#     )
#     await redis_client.expire(redis_key, 600)  # Cache for 10 minutes

#     return user  # повертаємо ORM-об'єкт


async def get_current_admin_user(current_user: UserSchema = Depends(get_current_user)):
    """
    Retrieves the current user and ensures they are an administrator.

    Args:
        current_user (UserSchema): The currently authenticated user.

    Returns:
        UserSchema: The current user if they are an admin.

    Raises:
        HTTPException: If the current user does not have admin rights.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Недостатньо прав доступу")
    return current_user

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, UserRole
from src.schemas import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        """
        Initializes the UserRepository with the provided database session.

        Args:
            session (AsyncSession): The asynchronous session for database operations.
        """
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User | None: A User object if found, or None if not found.
        """
        stmt = select(User).filter_by(id=user_id)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Retrieves a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User | None: A User object if found, or None if not found.
        """
        stmt = select(User).filter_by(username=username)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieves a user by their email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            User | None: A User object if found, or None if not found.
        """
        stmt = select(User).filter_by(email=email)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def create_user(self, body: UserCreate, avatar: str, role: UserRole) -> User:
        """
        Creates a new user in the database.

        Args:
            body (UserCreate): The user creation data.
            avatar (str): The URL or path to the user's avatar image.
            role (UserRole): The role assigned to the user (UserRole).

        Returns:
            User: The newly created User object.
        """
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar,
            role=role
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_avatar(self, user_id: int, new_avatar: str) -> User | None:
        """
        Updates the avatar of a user by their ID.

        Args:
            user_id (int): The ID of the user whose avatar is being updated.
            new_avatar (str): The new avatar URL or path.

        Returns:
            User | None: The updated User object if found, or None if not found.
        """
        user = await self.get_user_by_id(user_id)
        if user:
            user.avatar = new_avatar
            await self.db.commit()
            await self.db.refresh(user)
        return user

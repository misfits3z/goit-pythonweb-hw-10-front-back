from enum import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Date,
    Text,
    DateTime,
    func,
    ForeignKey,
    Boolean,
    Enum as SqlEnum,
)


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.

    This class serves as the foundation for defining ORM-mapped classes.
    """

    pass


class UserRole(str, Enum):
    """
    Enum class representing user roles.

    Attributes:
        USER (str): Regular user role.
        ADMIN (str): Administrator role.
    """

    USER = "user"
    ADMIN = "admin"


class Contact(Base):
    """
    Contact model for storing contact information.

    Attributes:
        id (int): Unique identifier for the contact.
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        email (str): Email address of the contact.
        phone_number (str): Phone number of the contact.
        birth_date (Date): Birth date of the contact.
        note (str): Optional notes about the contact.
        created_at (DateTime): Timestamp when the contact was created.
        updated_at (DateTime): Timestamp when the contact was last updated.
        user_id (int): Foreign key to the associated user (nullable).
        user (User): Relationship to the User model representing the owner of the contact.
    """

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    user = relationship("User", backref="contacts")


class User(Base):
    """
    User model for storing user account information.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for the user.
        hashed_password (str): Hashed password for authentication.
        email (str): Unique email address for the user.
        created_at (DateTime): Timestamp when the user account was created.
        avatar (str): URL to the user's avatar image (optional).
        is_verified (bool): Flag indicating if the user's email is verified.
        role (UserRole): Role of the user (either "user" or "admin").
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole), default=UserRole.USER, nullable=False
    )

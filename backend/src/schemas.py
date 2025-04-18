from datetime import date, datetime
from typing import  Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr, ConfigDict
from src.database.models import UserRole


# Модель для створення контакту
class ContactCreate(BaseModel):
    """
    A model for creating a contact.

    Attributes:
        first_name (str): The first name of the contact (max length 50).
        last_name (str): The last name of the contact (max length 50).
        email (str): The email of the contact (max length 50).
        phone_number (str): The phone number of the contact (max length 50).
        birth_date (date): The birth date of the contact.
        note (Optional[str]): An optional note for the contact (max length 250).
    """

    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: str = Field(..., max_length=255)
    phone_number: str = Field(..., max_length=20)
    birth_date: date
    note: Optional[str] = Field(default=None, max_length=250)

    model_config = ConfigDict(from_attributes=True)


# Модель для відповіді, що містить дані про контакт
class ContactResponse(ContactCreate):
    """
    A model for the contact response that contains detailed information.

    Attributes:
        id (int): The ID of the contact.
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (str): The email of the contact.
        phone_number (str): The phone number of the contact.
        birth_date (datetime): The birth date of the contact with time.
        note (Optional[str]): An optional note for the contact.
        created_at (Optional[datetime]): The creation timestamp of the contact.
        updated_at (Optional[datetime]): The last updated timestamp of the contact.
    """

    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    note: Optional[str] = None
    created_at: datetime | None
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


# Схема користувача
class User(BaseModel):
    """
    A model representing a user.

    Attributes:
        id (int): The ID of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        avatar (str): The avatar URL of the user.
        role (UserRole): The role of the user, defined in UserRole enum.
    """

    id: int
    username: str
    email: str
    avatar: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


# Схема для запиту реєстрації
class UserCreate(BaseModel):
    """
    A model for user registration request.

    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
    """

    username: str
    email: str
    password: str


# Схема для токену
class Token(BaseModel):
    """
    A model for the response containing an access token.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token, usually "bearer".
    """

    access_token: str
    refresh_token: str
    token_type: str


class RequestPasswordReset(BaseModel):
    """
    A model for the request to reset the password.

    Attributes:
        email (EmailStr): The email address of the user who is requesting the password reset.
    """

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """
    A model for confirming the password reset.

    Attributes:
        token (str): The token received for confirming the password reset.
        new_password (str): The new password (must be at least 6 characters long).
    """

    token: str
    new_password: str = Field(min_length=6)
    
class AvatarUpdateSchema(BaseModel):
    new_avatar: str


# # Модель для створення контакту
# class ContactCreate(BaseModel):
#     first_name: str = Field(..., max_length=50)
#     last_name: str = Field(..., max_length=50)
#     email: str = Field(max_length=50)
#     phone_number: str = Field(max_length=50)
#     birth_date: date
#     note: Optional[str] = Field(max_length=250)

#     class Config:
#         orm_mode = True


# # Модель для відповіді, що містить дані про контакт
# class ContactResponse(ContactCreate):
#     id: int
#     first_name: str
#     last_name: str
#     email: str
#     phone_number: str
#     birth_date: datetime
#     note: Optional[str] = None
#     created_at: datetime | None
#     updated_at: Optional[
#         datetime
#     ]
#     model_config = ConfigDict(from_attributes=True)


# # Схема користувача
# class User(BaseModel):
#     id: int
#     username: str
#     email: str
#     avatar: str
#     role: UserRole

#     model_config = ConfigDict(from_attributes=True)


# # Схема для запиту реєстрації
# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str
#     # role: UserRole


# # Схема для токену
# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class RequestPasswordReset(BaseModel):
#     email: EmailStr


# class PasswordResetConfirm(BaseModel):
#     token: str
#     new_password: str = Field(min_length=6)

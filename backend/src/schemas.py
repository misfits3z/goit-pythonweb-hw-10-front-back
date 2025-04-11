from datetime import date, datetime
from typing import  Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from src.database.models import UserRole


# Модель для створення контакту
class ContactCreate(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: str = Field(max_length=50)
    phone_number: str = Field(max_length=50)
    birth_date: date
    note: Optional[str] = Field(max_length=250)

    class Config:
        orm_mode = True


# Модель для відповіді, що містить дані про контакт
class ContactResponse(ContactCreate):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: datetime
    note: Optional[str] = None
    created_at: datetime | None  
    updated_at: Optional[
        datetime
    ] 
    model_config = ConfigDict(from_attributes=True)  


# Схема користувача
class User(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


# Схема для запиту реєстрації
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    # role: UserRole


# Схема для токену
class Token(BaseModel):
    access_token: str
    token_type: str


class RequestPasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=6)

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, Text, DateTime, func, ForeignKey, Column, Boolean

class Base(DeclarativeBase):
    pass


class Contact(Base):

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)  
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)  
    email: Mapped[str] = mapped_column(String(255), unique=True) 
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)  
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    note: Mapped[str] =  mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    user = relationship("User", backref="contacts")

# Модель Користувачів
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[DateTime] = mapped_column("created_at", DateTime, default=func.now())
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False)

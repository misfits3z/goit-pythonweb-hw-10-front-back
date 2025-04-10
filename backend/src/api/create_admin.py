from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas import UserCreate, User
from src.database.models import UserRole
from src.services.users import UserService
from src.database.db import get_db
from src.services.auth import get_current_admin_user  

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post(
    "/create-admin", response_model=User, status_code=status.HTTP_201_CREATED
)
async def create_admin(
    body: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user),  # перевірка ролі
):
    user_service = UserService(db)

    existing_user = await user_service.get_user_by_email(body.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Користувач з таким email уже існує"
        )

    new_admin = await user_service.create_user(body, role=UserRole.ADMIN)
    return new_admin

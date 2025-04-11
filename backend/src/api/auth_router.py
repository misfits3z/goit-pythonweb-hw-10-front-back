from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas import UserCreate, Token, User, RequestPasswordReset, PasswordResetConfirm
from src.services.auth import  Hash
from src.services.users import UserService
from src.database.db import get_db
from src.conf.config import config
from jose import jwt, JWTError
from src.utils.tokens import generate_password_reset_token, create_access_token


router  = APIRouter(tags=["auth"])


# Реєстрація користувача
@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)

    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач з таким email вже існує",
        )

    username_user = await user_service.get_user_by_username(user_data.username)
    if username_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач з таким іменем вже існує",
        )
    user_data.password = Hash().get_password_hash(user_data.password)
    new_user = await user_service.create_user(user_data)

    return new_user


# Логін користувача
@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний логін або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        email = payload["sub"]
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True  # Підтверджуємо email
    await db.commit()
    return {"message": "Email successfully verified"}


@router.post("/password-reset-email", status_code=status.HTTP_200_OK)
async def request_password_reset(
    body: RequestPasswordReset,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user_service = UserService(db)
    user = await user_service.get_user_by_email(body.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = generate_password_reset_token(user.email)

    background_tasks.add_task(user_service.send_password_reset_email, user.email, token)

    return {"message": "Password reset email sent"}


@router.post("/password-reset-confirm", status_code=status.HTTP_200_OK)
async def password_reset_confirm(
    data: PasswordResetConfirm, db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            data.token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        email = payload["sub"]
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = user_service.get_password_hash(data.new_password)
    await db.commit()

    return {"message": "Password reset successfully"}

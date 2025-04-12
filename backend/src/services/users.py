from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.repository.users import UserRepository
from src.schemas import UserCreate

import aiosmtplib
from email.mime.text import MIMEText
from src.conf.config import config
from src.utils.tokens import generate_verification_token
from src.database.models import UserRole


class UserService:
    """
    Service layer for managing user-related operations such as creating users,
    retrieving users by different fields, and sending emails for verification or password reset.
    """

    def __init__(self, db: AsyncSession):
        """
        Initializes the UserService with a database session.

        Args:
            db (AsyncSession): The database session used to interact with the repository.
        """
        self.repository = UserRepository(db)

    async def create_user(
        self, body: UserCreate, role: UserRole = UserRole.USER
    ):
        """
        Creates a new user, generates a verification token, and sends a verification email.

        Args:
            body (UserCreate): The data for creating the new user.
            role (UserRole, optional): The role assigned to the new user. Defaults to UserRole.USER.

        Returns:
            User: The newly created user.
        """
        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:
            print(e)

        user = await self.repository.create_user(body, avatar, role)

        # Generate a verification token
        token = await generate_verification_token(body.email)

        # Send the verification email
        await self.send_verification_email(body.email, token)

        return user

    async def get_user_by_id(self, user_id: int):
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User | None: The user object or None if not found.
        """
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str) :
        """
        Retrieves a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User | None: The user object or None if not found.
        """
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str) :
        """
        Retrieves a user by their email address.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            User | None: The user object or None if not found.
        """
        return await self.repository.get_user_by_email(email)

    async def send_verification_email(self, email: str, token: str):
        """
        Sends a verification email with a verification link to the specified email address.

        Args:
            email (str): The email address to send the verification link to.
            token (str): The verification token to include in the email link.
        """
        verify_link = f"http://localhost:8000/api/auth/verify-email?token={token}"
        msg = MIMEText(f"Click to verify your email: {verify_link}")
        msg["Subject"] = "Email Verification"
        msg["From"] = config.SMTP_USERNAME
        msg["To"] = email

        try:
            await aiosmtplib.send(
                message=msg.as_string(),
                hostname=config.SMTP_SERVER,
                port=config.SMTP_PORT,
                username=config.SMTP_USERNAME,
                password=config.SMTP_PASSWORD,
                start_tls=True,
            )
            print(f"✅ Verification email sent to {email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")

    async def send_password_reset_email(self, email: str, token: str):
        """
        Sends a password reset email with a reset link to the specified email address.

        Args:
            email (str): The email address to send the password reset link to.
            token (str): The token used to identify the password reset request.
        """
        reset_link = (
            f"http://localhost:3000/reset-password?token={token}"  # frontend route
        )
        msg = MIMEText(f"Click the link to reset your password: {reset_link}")
        msg["Subject"] = "Password Reset Request"
        msg["From"] = config.SMTP_USERNAME
        msg["To"] = email

        try:
            await aiosmtplib.send(
                message=msg.as_string(),
                hostname=config.SMTP_SERVER,
                port=config.SMTP_PORT,
                username=config.SMTP_USERNAME,
                password=config.SMTP_PASSWORD,
                start_tls=True,
            )
            print(f"✅ Password reset email sent to {email}")
        except Exception as e:
            print(f"❌ Failed to send password reset email: {e}")


# class UserService:
#     def __init__(self, db: AsyncSession):
#         self.repository = UserRepository(db)

#     async def create_user(self, body: UserCreate, role: UserRole = UserRole.USER):
#         avatar = None
#         try:
#             g = Gravatar(body.email)
#             avatar = g.get_image()
#         except Exception as e:
#             print(e)

#         user = await self.repository.create_user(body, avatar, role)

#         # Генеруємо verification token
#         token = await generate_verification_token(body.email)

#         # Надсилаємо email
#         await self.send_verification_email(body.email, token)

#         return user

#     async def get_user_by_id(self, user_id: int):
#         return await self.repository.get_user_by_id(user_id)

#     async def get_user_by_username(self, username: str):
#         return await self.repository.get_user_by_username(username)

#     async def get_user_by_email(self, email: str):
#         return await self.repository.get_user_by_email(email)

#     async def send_verification_email(self, email: str, token: str):
#         verify_link = f"http://localhost:8000/api/auth/verify-email?token={token}"
#         msg = MIMEText(f"Click to verify your email: {verify_link}")
#         msg["Subject"] = "Email Verification"
#         msg["From"] = config.SMTP_USERNAME
#         msg["To"] = email

#         try:
#             await aiosmtplib.send(
#                 message=msg.as_string(),
#                 hostname=config.SMTP_SERVER,
#                 port=config.SMTP_PORT,
#                 username=config.SMTP_USERNAME,
#                 password=config.SMTP_PASSWORD,
#                 start_tls=True,
#             )
#             print(f"✅ Verification email sent to {email}")
#         except Exception as e:
#             print(f"❌ Failed to send email: {e}")

#     async def send_password_reset_email(self, email: str, token: str):
#         reset_link = f"http://localhost:3000/reset-password?token={token}"  # frontend route
#         msg = MIMEText(f"Click the link to reset your password: {reset_link}")
#         msg["Subject"] = "Password Reset Request"
#         msg["From"] = config.SMTP_USERNAME
#         msg["To"] = email

#         try:
#             await aiosmtplib.send(
#                 message=msg.as_string(),
#                 hostname=config.SMTP_SERVER,
#                 port=config.SMTP_PORT,
#                 username=config.SMTP_USERNAME,
#                 password=config.SMTP_PASSWORD,
#                 start_tls=True,
#             )
#             print(f"✅ Password reset email sent to {email}")
#         except Exception as e:
#             print(f"❌ Failed to send password reset email: {e}")

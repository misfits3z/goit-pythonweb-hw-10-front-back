import os
from dotenv import load_dotenv

# Завантаження змінних середовища з .env
load_dotenv()


class Config:
    """
    Config class for application settings loaded from environment variables.

    Attributes:
        DB_URL (str): Database connection URL.
        JWT_SECRET (str): Secret key for encoding access JWTs.
        JWT_ALGORITHM (str): Algorithm used to sign JWT tokens.
        JWT_EXPIRATION_SECONDS (int): Lifetime of access JWTs in seconds.
        JWT_SECRET_REFRESH (str): Secret key for encoding refresh JWTs.
        JWT_REFRESH_EXPIRATION_SECONDS (int): Lifetime of refresh JWTs in seconds.
        SMTP_SERVER (str): SMTP server address for email sending.
        SMTP_PORT (int): Port used by the SMTP server.
        SMTP_USERNAME (str): SMTP username.
        SMTP_PASSWORD (str): SMTP password.
    """
    # Database
    DB_URL = os.getenv("DB_URL")

    # JWT Access Token
    JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-access-key")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_SECONDS = int(os.getenv("JWT_EXPIRATION_SECONDS", 3600))  # 1 година

    # JWT Refresh Token
    JWT_SECRET_REFRESH = os.getenv("JWT_SECRET_REFRESH", "super-secret-refresh-key")
    JWT_REFRESH_EXPIRATION_SECONDS = int(
        os.getenv("JWT_REFRESH_EXPIRATION_SECONDS", 7 * 24 * 60 * 60)
    )  # 7 днів

    # SMTP (Email)
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 2525))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "your_email@example.com")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_password")


config = Config()

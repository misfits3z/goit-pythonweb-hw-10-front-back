import os
from dotenv import load_dotenv

# Завантаження змінних середовища з .env
load_dotenv()


class Config:
    DB_URL = os.getenv("DB_URL")
    
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_SECONDS = int(os.getenv("JWT_EXPIRATION_SECONDS", 3600))

    # Додаємо SMTP
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 2525))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "your_email@example.com")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_password")


config = Config()

from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    ALVOCHAT_TOKEN: str
    ALVOCHAT_INSTANCE_ID: str
    ALVOCHAT_API_URL: str
    ALVOCHAT_WEBHOOK_URL: str
    DATABASE_URL: str = f"sqlite:///{Path(__file__).parent.parent}/whatsapp_bot.db"
    TEST_PHONE_NUMBER: str
    WEBHOOK_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()

print(f"Database URL: {settings.DATABASE_URL}")  # Add this line for debugging

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
print(f"ALVOCHAT_TOKEN: {settings.ALVOCHAT_TOKEN}")
print(f"ALVOCHAT_INSTANCE_ID: {settings.ALVOCHAT_INSTANCE_ID}")
print(f"ALVOCHAT_API_URL: {settings.ALVOCHAT_API_URL}")
print(f"ALVOCHAT_WEBHOOK_URL: {settings.ALVOCHAT_WEBHOOK_URL}")
print(f"DATABASE_URL: {settings.DATABASE_URL}")
print(f"TEST_PHONE_NUMBER: {settings.TEST_PHONE_NUMBER}")
print(f"WEBHOOK_TOKEN: {settings.WEBHOOK_TOKEN}")

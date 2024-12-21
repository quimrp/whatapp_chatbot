from pydantic import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os

# Carga manualmente el archivo .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

class Settings(BaseSettings):
    ALVOCHAT_TOKEN: str
    ALVOCHAT_INSTANCE_ID: str
    ALVOCHAT_API_URL: str
    ALVOCHAT_WEBHOOK_URL: str
    DATABASE_URL: str = f"sqlite:///{Path(__file__).parent.parent}/whatsapp_bot.db"
    TEST_PHONE_NUMBER: str
    WEBHOOK_TOKEN: str
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

print(f"Loaded WEBHOOK_TOKEN: {settings.WEBHOOK_TOKEN}")
print(f"Environment WEBHOOK_TOKEN: {os.environ.get('WEBHOOK_TOKEN')}")


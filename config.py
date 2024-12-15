from pydantic import BaseSettings, validator
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str

    # AWS Configuration
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_BUCKET_NAME: str

    # AlvoChat Configuration
    ALVOCHAT_TOKEN: str
    ALVOCHAT_INSTANCE_ID: str
    ALVOCHAT_API_URL: str
    ALVOCHAT_WEBHOOK_URL: str

    # App Configuration
    DEBUG: bool = False
    TEST_PHONE_NUMBER: str
    WEBHOOK_TOKEN: str

    @validator('ALVOCHAT_API_URL')
    def validate_alvochat_api_url(cls, v):
        if not v.startswith("https://"):
            raise ValueError("ALVOCHAT_API_URL debe comenzar con 'https://'")
        return v

    class Config:
        env_file = ".env"

settings = Settings()

# Print configuration (only in debug mode)
if settings.DEBUG:
    print("Configuración cargada:")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"AWS_BUCKET_NAME: {settings.AWS_BUCKET_NAME}")
    print(f"ALVOCHAT_API_URL: {settings.ALVOCHAT_API_URL}")
    print(f"ALVOCHAT_WEBHOOK_URL: {settings.ALVOCHAT_WEBHOOK_URL}")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"WEBHOOK_TOKEN: {settings.WEBHOOK_TOKEN[:5]}...") # Only print the first 5 characters for security


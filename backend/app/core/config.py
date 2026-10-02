from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Marrakech Drive API"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str
    REDIS_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_WHATSAPP_NUMBER: Optional[str] = None

    AI_API_KEY: Optional[str] = None
    AI_MODEL: str = "gpt-4o"

    FRONTEND_URL: str = "http://localhost:3000"

    # Added missing fields to prevent Pydantic ValidationError
    EMAIL_PROVIDER: Optional[str] = None
    EMAIL_API_KEY: Optional[str] = None
    ADMIN_SEED_PASSWORD: Optional[str] = None

    model_config = {
        "env_file": ".env",
        "extra": "ignore" # This allows extra variables in .env without failing
    }

settings = Settings()

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    upload_dir: str = "uploads/"
    EMAIL_HOST: Optional[str] = None
    EMAIL_PORT: Optional[int] = 587
    EMAIL_USER: Optional[str] = None
    EMAIL_PASS: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
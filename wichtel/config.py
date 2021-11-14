from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    MAILGUN_API_KEY: Optional[str]
    DEBUG: bool = True
    EMAIL: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

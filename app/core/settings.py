from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    TEST_DATABASE_URL: str
    # TEST_DATABASE_URL: str = "postgresql+asyncpg://app_user:app_password@localhost:5433/app_db"
    OPENAI_API_KEY: str

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-created_at"

    base_skill_url: Optional[str] = "/v1/skill"
    base_users_url: Optional[str] = "/v1/user"
    base_auth_route: Optional[str] = "/v1/auth"
    base_user_skills_route: Optional[str] = "/v1/user-skill"


settings = Settings()

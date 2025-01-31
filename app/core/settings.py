from typing import Optional

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=("dev.env", ".env"), env_file_encoding="utf-8")

    IS_PROD: bool

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    TEST_DATABASE_URL: Optional[str] = None

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-created_at"

    base_skill_url: Optional[str] = "/v1/skill"
    base_users_url: Optional[str] = "/v1/user"
    base_auth_route: Optional[str] = "/v1/auth"
    base_user_skills_route: Optional[str] = "/v1/user-skill"


settings = Settings()

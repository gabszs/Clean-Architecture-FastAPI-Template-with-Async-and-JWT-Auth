from typing import Optional

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "dev.env"), env_file_encoding="utf-8")

    PROJECT_NAME: str = "fastapi-auth"

    DATABASE_URL: str

    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 25

    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    TEST_DATABASE_URL: Optional[str] = None

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-created_at"

    # open-telemetry, please do not fill
    OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED: bool
    OTEL_EXPORTER_OTLP_ENDPOINT: str
    OTEL_EXPORTER_OTLP_INSECURE: str
    OTEL_LOGS_EXPORTER: str
    OTEL_SERVICE_NAME: str
    OTEL_EXPORTER_OTLP_PROTOCOL: str


settings = Settings()

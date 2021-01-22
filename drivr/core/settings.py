from secrets import token_urlsafe
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, validator
from pydantic.networks import AnyHttpUrl, PostgresDsn


class Settings(BaseSettings):
    """The environment variables of the app."""

    PROJECT_NAME: str = "drivr"
    PROJECT_VERSION: str = "0.1.0"

    # Server
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl

    # Secrets
    SECRET_KEY: str = token_urlsafe(32)

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def mount_cors_origins(
        cls,
        v: Union[str, List[str]],
    ) -> Union[List[str], str]:  # pragma: no cover
        """Mount the cors origins."""

        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "drivr"
    POSTGRES_PASSWORD: str = "drivr"
    POSTGRES_DB: str = "drivr"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def mount_database_connection(
        cls,
        v: Optional[str],
        values: Dict[str, Any],
    ) -> Any:  # pragma: no cover
        """Mount the database URL connection."""

        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True


settings = Settings()

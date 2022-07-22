from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator
from functools import lru_cache
from databases import DatabaseURL
import os


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
    MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
    MONGO_INITDB_ROOT_USERNAME: str = os.getenv(
        "MONGO_INITDB_ROOT_USERNAME", "whatsapp"
    )
    MONGO_INITDB_ROOT_PASSWORD: str = os.getenv(
        "MONGO_INITDB_ROOT_PASSWORD", "password"
    )
    MONGO_DATABASE_NAME: str = os.getenv("MONGO_DATABASE_NAME", "whatsapp")
    MONGO_HOST: str = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT: int = int(os.getenv("MONGO_PORT", 27017))
    DATABASE_URI: Optional[DatabaseURL] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return DatabaseURL(
            f'mongodb://{values.get("MONGO_INITDB_ROOT_USERNAME")}:{values.get("MONGO_INITDB_ROOT_PASSWORD")}@{values.get("MONGO_HOST")}:{values.get("MONGO_PORT")}/{values.get("MONGO_DATABASE_NAME")}?authSource=admin'
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()

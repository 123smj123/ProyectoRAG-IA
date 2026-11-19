from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/core/config.py -> raíz del repositorio
BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    upload_dir: Path = Path("data/uploads")
    max_upload_size_mb: int = 20
    chunk_size: int = 700
    chunk_overlap: int = 100

    @model_validator(mode="after")
    def check_chunk_settings(self) -> "Settings":
        if self.chunk_size <= 0:
            raise ValueError("CHUNK_SIZE debe ser mayor que 0")
        if not 0 <= self.chunk_overlap < self.chunk_size:
            raise ValueError("CHUNK_OVERLAP debe estar entre 0 y CHUNK_SIZE - 1")
        return self


settings = Settings()

UPLOAD_PATH = BASE_DIR / settings.upload_dir
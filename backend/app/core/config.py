from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/core/config.py -> raíz del repositorio
BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    upload_dir: Path = Path("data/uploads")
    max_upload_size_mb: int = 20


settings = Settings()

UPLOAD_PATH = BASE_DIR / settings.upload_dir
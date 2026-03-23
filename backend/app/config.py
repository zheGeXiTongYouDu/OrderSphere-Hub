from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "OrderSphere-Hub"
    backend_cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    database_url: str = f"sqlite:///{BASE_DIR.parent / 'db' / 'ordersphere.db'}"

    class Config:
        env_file = ".env"


settings = Settings()

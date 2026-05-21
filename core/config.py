import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL", "").strip()
    if database_url:
        return database_url
    return f"sqlite:///{DATA_DIR / 'ngoding_lab.db'}"


APP_ENV = os.getenv("APP_ENV", "development")

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import get_database_url


Base = declarative_base()


def _normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg2://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


DATABASE_URL = _normalize_database_url(get_database_url())
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    from core import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db():
    return SessionLocal()

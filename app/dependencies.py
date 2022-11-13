from contextlib import contextmanager
from typing import Generator

from app.database import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_context = contextmanager(get_db)

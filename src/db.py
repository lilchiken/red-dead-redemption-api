from typing import Generator
from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(
    os.getenv(...),
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


def get_db() -> Generator:
    """Dependency for getting async session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

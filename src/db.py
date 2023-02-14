from typing import Generator
from dotenv import load_dotenv
# import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(
    # os.getenv(...),
    "postgresql://test_admin:0000@localhost:5432/testing_table"
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=True,
    autoflush=True
)


def get_db() -> Generator:
    """Dependency for getting async session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

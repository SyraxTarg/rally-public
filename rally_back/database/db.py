"""
This file contains the database related functions
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL, future=True, echo=True, connect_args={"check_same_thread": False})

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://root:root@localhost:5432/rally")

engine = create_engine(DATABASE_URL, future=True, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Provides a database session.

    This function creates and returns a database session that can be used to interact with the database.
    The session is automatically closed after the interaction is complete, even if an exception occurs.

    Yields:
        Session: A database session for interacting with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
Database Connection
Handle database connections and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from ..core.config import settings

# Create database engine
# For PostgreSQL with psycopg2 (sync), we'll use a different approach
database_url = settings.database_url
if "postgresql" in database_url and "asyncpg" in database_url:
    # Use sync PostgreSQL for startup operations
    sync_database_url = database_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
    engine = create_engine(sync_database_url)
elif "postgresql" in database_url:
    # Already using psycopg2
    engine = create_engine(database_url)
else:
    # Use SQLite for development
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for database sessions
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database"""
    try:
        # Import all models here to ensure they are registered
        from ..models.database import Base
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise


def get_db_session() -> Session:
    """
    Get a database session
    
    Returns:
        Session: Database session
    """
    return SessionLocal()
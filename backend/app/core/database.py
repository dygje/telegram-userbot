"""
Database Connection
Handle database connections and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import asyncio
from ..core.config import settings

# Create database engine
# For PostgreSQL with asyncpg, we need to use a different approach
# But for simplicity in this context, we'll use SQLite for development
if "postgresql" in settings.database_url:
    # For PostgreSQL, we'll use a sync engine for initialization
    # In production, you would use asyncpg properly with async/await
    engine = create_engine(
        settings.database_url.replace("postgresql+asyncpg", "postgresql+psycopg2"),
        connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
    )
else:
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
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
"""
Database Module
Handles database connections and initialization
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Create base class for models
Base = declarative_base()

# Create engine - switching to sync engine to avoid async issues in init_db

# Check if database URL is async and convert to sync if needed
db_url = settings.database_url
if db_url.startswith("sqlite+aiosqlite"):
    db_url = db_url.replace("sqlite+aiosqlite", "sqlite")

engine = create_engine(db_url)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """
    Get database session
    """
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        print(f"Error getting database session: {e}")
        db.close()
        raise


def init_db():
    """
    Initialize database tables
    """
    try:
        # Import models to register them with Base.metadata
        from app.models.database import Group, Message, BlacklistedChat, Config

        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables initialized successfully")
    except Exception as e:
        print(f"Error initializing database tables: {e}")
        raise

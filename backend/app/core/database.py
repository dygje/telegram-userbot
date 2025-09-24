"""
Database Module
Handles database connections and initialization
"""

from sqlalchemy.orm import sessionmaker
from .config import settings

# Import Base from models to ensure we use the same metadata
from app.models.database import Base

# Create engine - switching to sync engine to avoid async issues in init_db

# Check if database URL is async and convert to sync if needed
db_url = settings.database_url
if db_url.startswith("sqlite+aiosqlite"):
    db_url = db_url.replace("sqlite+aiosqlite", "sqlite")

from sqlalchemy import create_engine
# Create engine with the potentially converted URL
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
        # Check the current database URL
        print(f"Initializing database with URL from settings: {settings.database_url}")
        
        # Import models to register them with Base.metadata
        # These imports are intentionally kept to ensure models are registered
        import app.models.database  # noqa: F401
        
        # Check if database URL is async and convert to sync if needed
        db_url = settings.database_url
        if db_url.startswith("sqlite+aiosqlite"):
            db_url = db_url.replace("sqlite+aiosqlite", "sqlite")
        
        print(f"Using converted URL: {db_url}")
        
        # Create a temporary engine to ensure we're using the right connection
        from sqlalchemy import create_engine
        temp_engine = create_engine(db_url)
        
        # Create all tables with the temporary engine
        Base.metadata.create_all(bind=temp_engine)
        print("Database tables initialized successfully")
        
        # Close the temporary engine
        temp_engine.dispose()
    except Exception as e:
        print(f"Error initializing database tables: {e}")
        raise
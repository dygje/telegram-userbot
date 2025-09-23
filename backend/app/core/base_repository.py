"""
Base Repository Class
Provides common functionality for all repository classes
"""

from typing import TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from ..core.database import get_db_session

T = TypeVar('T')  # Generic type variable for model classes

class BaseRepository(Generic[T]):
    """Base repository class with common CRUD operations"""
    
    def __init__(self, model_class: T, db: Session = None):
        self.model_class = model_class
        self.db = db or get_db_session()
    
    def get_all(self, filter_active: bool = True) -> List[T]:
        """Get all records"""
        query = self.db.query(self.model_class)
        if filter_active and hasattr(self.model_class, 'is_active'):
            query = query.filter(self.model_class.is_active.is_(True))
        return query.all()
    
    def get_by_id(self, id: int, filter_active: bool = True) -> Optional[T]:
        """Get record by ID"""
        query = self.db.query(self.model_class).filter(self.model_class.id == id)
        if filter_active and hasattr(self.model_class, 'is_active'):
            query = query.filter(self.model_class.is_active.is_(True))
        return query.first()
    
    def create(self, **kwargs) -> T:
        """Create a new record"""
        try:
            record = self.model_class(**kwargs)
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            return record
        except Exception as e:
            self.db.rollback()
            raise e
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Update a record"""
        record = self.get_by_id(id, filter_active=False)
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
            if hasattr(record, 'updated_at'):
                record.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(record)
        return record
    
    def delete(self, id: int, soft_delete: bool = True) -> bool:
        """Delete a record"""
        record = self.get_by_id(id, filter_active=False)
        if record:
            if soft_delete and hasattr(record, 'is_active'):
                record.is_active = False
                if hasattr(record, 'updated_at'):
                    record.updated_at = datetime.utcnow()
            else:
                self.db.delete(record)
            self.db.commit()
            return True
        return False
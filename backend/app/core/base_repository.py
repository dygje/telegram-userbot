"""
Base Repository Module
Contains the base repository class with common database operations
"""

from typing import Type, Generic, Optional, List, Dict, Any, TypeVar
from sqlalchemy.orm import Session
from app.models.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=Base)  # type: ignore


class BaseRepository(Generic[T]):
    """
    Base repository class with common database operations
    """

    def __init__(self, model: Type[T], db: Optional[Session] = None):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[T]:
        if self.db is None:
            raise ValueError("Database session not provided")
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[T]:
        if self.db is None:
            raise ValueError("Database session not provided")
        return self.db.query(self.model).all()

    def create(self, obj_data: Dict[str, Any]) -> T:
        if self.db is None:
            raise ValueError("Database session not provided")
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: int, obj_data: Dict[str, Any]) -> Optional[T]:
        if self.db is None:
            raise ValueError("Database session not provided")
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        if self.db is None:
            raise ValueError("Database session not provided")
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        self.db.delete(db_obj)
        self.db.commit()
        return True

"""
Repository Module
Contains specific repository classes for each model
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from app.models.database import Group, Message, BlacklistedChat, Config
from datetime import datetime


class GroupRepository(BaseRepository[Group]):
    """
    Repository class for Group model
    """

    def __init__(self, db: Optional[Session] = None):
        super().__init__(Group, db)

    def get_group_by_identifier(self, identifier: str) -> Optional[Group]:
        """Get a group by its identifier"""
        if self.db is None:
            raise ValueError("Database session not provided")
        return (
            self.db.query(self.model)
            .filter(self.model.identifier == identifier)
            .first()
        )

    def get_all_groups(self) -> List[Group]:
        """Get all groups"""
        if self.db is None:
            raise ValueError("Database session not provided")
        return self.db.query(self.model).all()

    def create_group(self, identifier: str) -> Group:
        """Create a new group"""
        if self.db is None:
            raise ValueError("Database session not provided")
        group = Group(identifier=identifier)
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def delete_group(self, group_id: int) -> bool:
        """Delete a group by ID"""
        return self.delete(group_id)


class MessageRepository(BaseRepository[Message]):
    """
    Repository class for Message model
    """

    def __init__(self, db: Optional[Session] = None):
        super().__init__(Message, db)

    def get_all_messages(self) -> List[Message]:
        """Get all messages"""
        if self.db is None:
            raise ValueError("Database session not provided")
        return self.db.query(self.model).all()

    def create_message(self, text: str) -> Message:
        """Create a new message"""
        if self.db is None:
            raise ValueError("Database session not provided")
        message = Message(text=text)
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def delete_message(self, message_id: int) -> bool:
        """Delete a message by ID"""
        return self.delete(message_id)


class BlacklistRepository(BaseRepository[BlacklistedChat]):
    """
    Repository class for BlacklistedChat model
    """

    def __init__(self, db: Optional[Session] = None):
        super().__init__(BlacklistedChat, db)

    def get_all_blacklisted_chats(self) -> List[BlacklistedChat]:
        """Get all blacklisted chats"""
        if self.db is None:
            raise ValueError("Database session not provided")
        return self.db.query(self.model).all()

    def get_blacklisted_chat_by_id(self, chat_id: str) -> Optional[BlacklistedChat]:
        """Get a blacklisted chat by its ID"""
        if self.db is None:
            raise ValueError("Database session not provided")
        return self.db.query(self.model).filter(self.model.chat_id == chat_id).first()

    def add_to_blacklist(
        self, chat_id: str, reason: str, is_permanent: bool = True, expiry_time=None
    ) -> BlacklistedChat:
        """Add a chat to the blacklist"""
        if self.db is None:
            raise ValueError("Database session not provided")
        blacklisted_chat = BlacklistedChat(
            chat_id=chat_id,
            reason=reason,
            is_permanent=is_permanent,
            expiry_time=expiry_time,
        )
        self.db.add(blacklisted_chat)
        self.db.commit()
        self.db.refresh(blacklisted_chat)
        return blacklisted_chat

    def remove_from_blacklist(self, chat_id: str) -> bool:
        """Remove a chat from the blacklist"""
        if self.db is None:
            raise ValueError("Database session not provided")
        blacklisted_chat = self.get_blacklisted_chat_by_id(chat_id)
        if not blacklisted_chat:
            return False
        self.db.delete(blacklisted_chat)
        self.db.commit()
        return True

    def is_blacklisted(self, chat_id: str) -> bool:
        """Check if a chat is blacklisted"""
        blacklisted_chat = self.get_blacklisted_chat_by_id(chat_id)
        if not blacklisted_chat:
            return False
        if not blacklisted_chat.is_permanent and blacklisted_chat.expiry_time:
            from datetime import datetime

            if blacklisted_chat.expiry_time < datetime.utcnow():
                # Entry has expired, remove it from blacklist
                self.remove_from_blacklist(chat_id)
                return False
        return True

    def clean_expired_blacklist(self) -> int:
        """Clean expired temporary blacklist entries"""
        if self.db is None:
            raise ValueError("Database session not provided")
        from sqlalchemy import and_

        expired_chats = (
            self.db.query(self.model)
            .filter(
                self.model.is_permanent.is_(False),
                self.model.expiry_time < datetime.utcnow(),
            )
            .all()
        )

        count = 0
        for chat in expired_chats:
            self.db.delete(chat)
            count += 1

        if count > 0:
            self.db.commit()

        return count


class ConfigRepository(BaseRepository[Config]):
    """
    Repository class for Config model
    """

    def __init__(self, db: Optional[Session] = None):
        super().__init__(Config, db)

    def get_config_by_key(self, key: str) -> Optional[Config]:
        """Get a config by its key"""
        if self.db is None:
            raise ValueError("Database session not provided")
        return self.db.query(self.model).filter(self.model.key == key).first()

    def get_config_value(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a config value by its key, with optional default"""
        config = self.get_config_by_key(key)
        if config:
            return config.value
        return default

    def set_config(self, key: str, value: str, description: Optional[str] = None) -> Config:
        """Set a config value"""
        if self.db is None:
            raise ValueError("Database session not provided")
        config = self.get_config_by_key(key)
        if config:
            config.value = value
            if description:
                config.description = description
        else:
            # Mypy berpikir assignment langsung ke field Column tidak valid
            # Tapi ini perilaku standar SQLAlchemy
            config = Config(key=key, value=value, description=description)
            self.db.add(config)
        self.db.commit()
        self.db.refresh(config)
        return config

    def get_all_configs(self) -> List[Config]:
        """Get all configuration settings"""
        if self.db is None:
            raise ValueError("Database session not provided")
        return self.db.query(self.model).all()

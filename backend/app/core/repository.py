"""
Repository Pattern Implementation
Data access layer for the Telegram userbot
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from ..models.database import Group, Message, BlacklistedChat, Config
from ..core.database import get_db_session
from ..core.base_repository import BaseRepository


class GroupRepository(BaseRepository[Group]):
    """Repository for Group model"""

    def __init__(self, db: Session = None):
        super().__init__(Group, db)

    def get_all_groups(self) -> List[Group]:
        """Get all active groups"""
        return self.get_all()

    def get_group_by_identifier(self, identifier: str) -> Optional[Group]:
        """Get group by identifier"""
        return (
            self.db.query(Group)
            .filter(and_(Group.identifier == identifier, Group.is_active.is_(True)))
            .first()
        )

    def create_group(self, identifier: str, name: Optional[str] = None) -> Group:
        """Create a new group"""
        return self.create(identifier=identifier, name=name or identifier)

    def update_group(self, group_id: int, **kwargs) -> Optional[Group]:
        """Update a group"""
        return self.update(group_id, **kwargs)

    def delete_group(self, group_id: int) -> bool:
        """Delete a group (soft delete)"""
        return self.delete(group_id)

    def bulk_create_groups(self, identifiers: List[str]) -> List[Group]:
        """Create multiple groups"""
        groups = []
        for identifier in identifiers:
            group = self.get_group_by_identifier(identifier)
            if not group:
                group = self.create_group(identifier)
            groups.append(group)
        return groups


class MessageRepository(BaseRepository[Message]):
    """Repository for Message model"""

    def __init__(self, db: Session = None):
        super().__init__(Message, db)

    def get_all_messages(self) -> List[Message]:
        """Get all active messages"""
        return self.get_all()

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        """Get message by ID"""
        return self.get_by_id(message_id)

    def create_message(self, text: str) -> Message:
        """Create a new message"""
        return self.create(text=text)

    def update_message(self, message_id: int, **kwargs) -> Optional[Message]:
        """Update a message"""
        return self.update(message_id, **kwargs)

    def delete_message(self, message_id: int) -> bool:
        """Delete a message (soft delete)"""
        return self.delete(message_id)


class BlacklistRepository(BaseRepository[BlacklistedChat]):
    """Repository for BlacklistedChat model"""

    def __init__(self, db: Session = None):
        super().__init__(BlacklistedChat, db)

    def get_all_blacklisted_chats(self) -> List[BlacklistedChat]:
        """Get all blacklisted chats"""
        return self.get_all(filter_active=False)

    def get_blacklisted_chat_by_chat_id(
        self, chat_id: str
    ) -> Optional[BlacklistedChat]:
        """Get blacklisted chat by chat ID"""
        return (
            self.db.query(BlacklistedChat)
            .filter(BlacklistedChat.chat_id == chat_id)
            .first()
        )

    def add_to_blacklist(
        self,
        chat_id: str,
        reason: str,
        is_permanent: bool = False,
        expiry_time: Optional[datetime] = None,
    ) -> BlacklistedChat:
        """Add a chat to blacklist"""
        return self.create(
            chat_id=chat_id,
            reason=reason,
            is_permanent=is_permanent,
            expiry_time=expiry_time,
        )

    def remove_from_blacklist(self, chat_id: str) -> bool:
        """Remove a chat from blacklist"""
        blacklisted_chat = self.get_blacklisted_chat_by_chat_id(chat_id)
        if blacklisted_chat:
            self.db.delete(blacklisted_chat)
            self.db.commit()
            return True
        return False

    def clean_expired_blacklist(self) -> int:
        """Clean expired temporary blacklist entries"""
        current_time = datetime.utcnow()
        expired_chats = (
            self.db.query(BlacklistedChat)
            .filter(
                and_(
                    BlacklistedChat.is_permanent == False,
                    BlacklistedChat.expiry_time < current_time,
                )
            )
            .all()
        )

        count = len(expired_chats)
        for chat in expired_chats:
            self.db.delete(chat)

        self.db.commit()
        return count

    def is_blacklisted(self, chat_id: str) -> bool:
        """Check if a chat is blacklisted"""
        blacklisted_chat = self.get_blacklisted_chat_by_chat_id(chat_id)

        if not blacklisted_chat:
            return False

        # Check if temporary blacklist has expired
        if not blacklisted_chat.is_permanent:
            if blacklisted_chat.expiry_time < datetime.utcnow():
                # Remove expired entry
                self.db.delete(blacklisted_chat)
                self.db.commit()
                return False

        return True


class ConfigRepository(BaseRepository[Config]):
    """Repository for Config model"""

    def __init__(self, db: Session = None):
        super().__init__(Config, db)

    def get_all_configs(self) -> List[Config]:
        """Get all configurations"""
        return self.get_all(filter_active=False)

    def get_config_by_key(self, key: str) -> Optional[Config]:
        """Get configuration by key"""
        return self.db.query(Config).filter(Config.key == key).first()

    def set_config(
        self, key: str, value: str, description: Optional[str] = None
    ) -> Config:
        """Set configuration value"""
        try:
            config = self.get_config_by_key(key)
            if config:
                config.value = value
                config.description = description
                if hasattr(config, "updated_at"):
                    config.updated_at = datetime.utcnow()
            else:
                config = Config(key=key, value=value, description=description)
                self.db.add(config)

            self.db.commit()
            self.db.refresh(config)
            return config
        except Exception as e:
            self.db.rollback()
            raise e

    def get_config_value(self, key: str, default: Optional[str] = None) -> str:
        """Get configuration value"""
        config = self.get_config_by_key(key)
        return config.value if config else (default or "")

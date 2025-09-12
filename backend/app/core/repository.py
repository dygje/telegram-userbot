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


class GroupRepository:
    """Repository for Group model"""
    
    def __init__(self, db: Session = None):
        self.db = db or get_db_session()
    
    def get_all_groups(self) -> List[Group]:
        """Get all active groups"""
        return self.db.query(Group).filter(Group.is_active == True).all()
    
    def get_group_by_identifier(self, identifier: str) -> Optional[Group]:
        """Get group by identifier"""
        return self.db.query(Group).filter(
            and_(Group.identifier == identifier, Group.is_active == True)
        ).first()
    
    def create_group(self, identifier: str, name: str = None) -> Group:
        """Create a new group"""
        try:
            group = Group(identifier=identifier, name=name or identifier)
            self.db.add(group)
            self.db.commit()
            self.db.refresh(group)
            return group
        except Exception as e:
            self.db.rollback()
            raise e
    
    def update_group(self, group_id: int, **kwargs) -> Optional[Group]:
        """Update a group"""
        group = self.db.query(Group).filter(Group.id == group_id).first()
        if group:
            for key, value in kwargs.items():
                setattr(group, key, value)
            group.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(group)
        return group
    
    def delete_group(self, group_id: int) -> bool:
        """Delete a group (soft delete)"""
        group = self.db.query(Group).filter(Group.id == group_id).first()
        if group:
            group.is_active = False
            group.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
    
    def bulk_create_groups(self, identifiers: List[str]) -> List[Group]:
        """Create multiple groups"""
        groups = []
        for identifier in identifiers:
            group = self.get_group_by_identifier(identifier)
            if not group:
                group = self.create_group(identifier)
            groups.append(group)
        return groups


class MessageRepository:
    """Repository for Message model"""
    
    def __init__(self, db: Session = None):
        self.db = db or get_db_session()
    
    def get_all_messages(self) -> List[Message]:
        """Get all active messages"""
        return self.db.query(Message).filter(Message.is_active == True).all()
    
    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        """Get message by ID"""
        return self.db.query(Message).filter(
            and_(Message.id == message_id, Message.is_active == True)
        ).first()
    
    def create_message(self, text: str) -> Message:
        """Create a new message"""
        try:
            message = Message(text=text)
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)
            return message
        except Exception as e:
            self.db.rollback()
            raise e
    
    def update_message(self, message_id: int, **kwargs) -> Optional[Message]:
        """Update a message"""
        message = self.db.query(Message).filter(Message.id == message_id).first()
        if message:
            for key, value in kwargs.items():
                setattr(message, key, value)
            message.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(message)
        return message
    
    def delete_message(self, message_id: int) -> bool:
        """Delete a message (soft delete)"""
        message = self.db.query(Message).filter(Message.id == message_id).first()
        if message:
            message.is_active = False
            message.updated_at = datetime.utcnow()
            self.db.commit()
            return True
        return False


class BlacklistRepository:
    """Repository for BlacklistedChat model"""
    
    def __init__(self, db: Session = None):
        self.db = db or get_db_session()
    
    def get_all_blacklisted_chats(self) -> List[BlacklistedChat]:
        """Get all blacklisted chats"""
        return self.db.query(BlacklistedChat).all()
    
    def get_blacklisted_chat_by_chat_id(self, chat_id: str) -> Optional[BlacklistedChat]:
        """Get blacklisted chat by chat ID"""
        return self.db.query(BlacklistedChat).filter(BlacklistedChat.chat_id == chat_id).first()
    
    def add_to_blacklist(self, chat_id: str, reason: str, is_permanent: bool = False, 
                        expiry_time: datetime = None) -> BlacklistedChat:
        """Add a chat to blacklist"""
        blacklisted_chat = BlacklistedChat(
            chat_id=chat_id,
            reason=reason,
            is_permanent=is_permanent,
            expiry_time=expiry_time
        )
        self.db.add(blacklisted_chat)
        self.db.commit()
        self.db.refresh(blacklisted_chat)
        return blacklisted_chat
    
    def remove_from_blacklist(self, chat_id: str) -> bool:
        """Remove a chat from blacklist"""
        blacklisted_chat = self.db.query(BlacklistedChat).filter(
            BlacklistedChat.chat_id == chat_id
        ).first()
        if blacklisted_chat:
            self.db.delete(blacklisted_chat)
            self.db.commit()
            return True
        return False
    
    def clean_expired_blacklist(self) -> int:
        """Clean expired temporary blacklist entries"""
        current_time = datetime.utcnow()
        expired_chats = self.db.query(BlacklistedChat).filter(
            and_(
                BlacklistedChat.is_permanent == False,
                BlacklistedChat.expiry_time < current_time
            )
        ).all()
        
        count = len(expired_chats)
        for chat in expired_chats:
            self.db.delete(chat)
        
        self.db.commit()
        return count
    
    def is_blacklisted(self, chat_id: str) -> bool:
        """Check if a chat is blacklisted"""
        blacklisted_chat = self.db.query(BlacklistedChat).filter(
            BlacklistedChat.chat_id == chat_id
        ).first()
        
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


class ConfigRepository:
    """Repository for Config model"""
    
    def __init__(self, db: Session = None):
        self.db = db or get_db_session()
    
    def get_all_configs(self) -> List[Config]:
        """Get all configurations"""
        return self.db.query(Config).all()
    
    def get_config_by_key(self, key: str) -> Optional[Config]:
        """Get configuration by key"""
        return self.db.query(Config).filter(Config.key == key).first()
    
    def set_config(self, key: str, value: str, description: str = None) -> Config:
        """Set configuration value"""
        try:
            config = self.get_config_by_key(key)
            if config:
                config.value = value
                config.description = description
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
    
    def get_config_value(self, key: str, default: str = None) -> str:
        """Get configuration value"""
        config = self.get_config_by_key(key)
        return config.value if config else default


# Example usage
if __name__ == "__main__":
    # Initialize repositories
    group_repo = GroupRepository()
    message_repo = MessageRepository()
    blacklist_repo = BlacklistRepository()
    config_repo = ConfigRepository()
    
    # Example operations
    # group = group_repo.create_group("@testgroup", "Test Group")
    # message = message_repo.create_message("Hello, this is a test message!")
    # config = config_repo.set_config("message_interval", "5-10", "Message interval in seconds")
"""
Database Models
SQLAlchemy models for the Telegram userbot
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Group(Base):
    """Model for managed Telegram groups"""
    
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True)  # Link, username, or ID
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Group(id={self.id}, identifier='{self.identifier}', name='{self.name}')>"


class Message(Base):
    """Model for messages to be sent"""
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Message(id={self.id}, text='{self.text[:50]}...')>"


class BlacklistedChat(Base):
    """Model for blacklisted chats"""
    
    __tablename__ = "blacklisted_chats"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, index=True)
    reason = Column(String)
    is_permanent = Column(Boolean, default=False)
    expiry_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<BlacklistedChat(chat_id='{self.chat_id}', reason='{self.reason}')>"


class Config(Base):
    """Model for configuration settings"""
    
    __tablename__ = "config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Config(key='{self.key}', value='{self.value}')>"
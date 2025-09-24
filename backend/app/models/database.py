"""
Database Models Module
Contains all SQLAlchemy database models for the application
"""

# mypy: disable-error-code="valid-type,misc"

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base
import datetime

# Base class for all models
Base = declarative_base()  # type: ignore


class Group(Base):
    """
    Group model for storing managed group information
    """

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)  # Will be fetched from Telegram API


class Message(Base):
    """
    Message model for storing messages to be sent
    """

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class BlacklistedChat(Base):
    """
    BlacklistedChat model for storing blacklisted chat information
    """

    __tablename__ = "blacklisted_chats"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, index=True, nullable=False)
    reason = Column(String, nullable=False)
    is_permanent = Column(Boolean, default=False)
    expiry_time = Column(DateTime, nullable=True)  # For temporary blacklists


class Config(Base):
    """
    Config model for storing configuration settings
    """

    __tablename__ = "config"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(String, nullable=False)
    description = Column(String, nullable=True)

"""
Configuration Management Module
Handles loading and validation of environment variables
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Telegram API credentials
    telegram_api_id: int
    telegram_api_hash: str
    phone_number: Optional[str] = None

    # Session management
    session_string: Optional[str] = None

    # Security
    secret_key: str

    # Database
    database_url: str

    # TMA Web UI
    next_public_api_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # No need to define env_prefix as empty string anymore
    )

    @field_validator("telegram_api_id")
    def validate_api_id(cls, v):
        """Validate Telegram API ID"""
        if not v:
            raise ValueError("TELEGRAM_API_ID is required")
        return v

    @field_validator("telegram_api_hash")
    def validate_api_hash(cls, v):
        """Validate Telegram API Hash"""
        if not v:
            raise ValueError("TELEGRAM_API_HASH is required")
        return v

    @field_validator("secret_key")
    def validate_secret_key(cls, v):
        """Validate secret key"""
        if not v:
            raise ValueError("SECRET_KEY is required")
        return v


# Settings instance will be created automatically from environment variables
settings = Settings()

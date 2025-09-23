"""
Test file for the Telegram Userbot backend
"""

import pytest
import os
from fastapi.testclient import TestClient

# Set test environment variables before importing app
os.environ["TELEGRAM_API_ID"] = "123456"
os.environ["TELEGRAM_API_HASH"] = "test_hash"
os.environ["SECRET_KEY"] = "test_secret_key_32_characters_min"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_telegram_bot.db"

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Telegram Userbot TMA API"}


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


if __name__ == "__main__":
    pytest.main([__file__])
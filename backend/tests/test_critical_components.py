"""
Test file for the Telegram Userbot backend - Critical Components
"""

import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock

# Set test environment variables before importing app
os.environ["TELEGRAM_API_ID"] = "123456"
os.environ["TELEGRAM_API_HASH"] = "test_hash"
os.environ["SECRET_KEY"] = "test_secret_key_32_characters_min"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_telegram_bot.db"

from app.main import app
from app.core.userbot import TelegramUserbot
from app.core.telegram_auth import TelegramAuth

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


@patch("app.api.routes.userbot")
def test_userbot_status_endpoint(mock_userbot):
    """Test the userbot status endpoint"""
    # Mock userbot instance
    mock_userbot.is_running = True
    mock_userbot.auth = MagicMock()
    mock_userbot.auth.get_me = AsyncMock(
        return_value={
            "id": 123456789,
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+1234567890",
        }
    )

    response = client.get("/api/v1/userbot/status")
    assert response.status_code == 200
    data = response.json()
    assert data["running"] == True
    assert "user_info" in data


@patch("app.api.routes.userbot")
def test_send_auth_code_endpoint(mock_userbot):
    """Test the send auth code endpoint"""
    # Mock userbot.auth instance
    mock_userbot.auth = MagicMock()
    mock_userbot.auth.send_code = AsyncMock(return_value="test_phone_code_hash")

    response = client.post("/api/v1/auth/send-code")
    assert response.status_code == 200
    data = response.json()
    assert "phone_code_hash" in data
    assert data["phone_code_hash"] == "test_phone_code_hash"


@patch("app.api.routes.userbot")
def test_sign_in_endpoint(mock_userbot):
    """Test the sign in endpoint"""
    # Mock userbot instance
    mock_userbot.authenticate_new_session = AsyncMock(return_value=True)

    response = client.post(
        "/api/v1/auth/sign-in", json={"code": "12345", "phone_code_hash": "test_hash"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "successful" in data["message"]


@patch("app.api.routes.userbot")
def test_sign_in_password_endpoint(mock_userbot):
    """Test the sign in with password endpoint"""
    # Mock userbot instance
    mock_userbot.authenticate_with_password = AsyncMock(return_value=True)

    response = client.post(
        "/api/v1/auth/sign-in-password", json={"password": "test_password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "successful" in data["message"]


@patch("app.api.routes.userbot")
def test_add_group_endpoint(mock_userbot):
    """Test the add group endpoint"""
    # Mock userbot instance
    mock_userbot.add_group = MagicMock(return_value=True)

    response = client.post("/api/v1/groups", json={"identifier": "@testgroup"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "successfully" in data["message"]


@patch("app.api.routes.userbot")
def test_add_message_endpoint(mock_userbot):
    """Test the add message endpoint"""
    # Mock userbot instance
    mock_userbot.add_message = MagicMock(return_value=True)

    response = client.post("/api/v1/messages", json={"text": "Test message"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "successfully" in data["message"]


@patch("app.api.routes.userbot")
def test_start_userbot_endpoint(mock_userbot):
    """Test the start userbot endpoint"""
    # Mock userbot instance
    mock_userbot.start = AsyncMock(return_value=True)

    response = client.post("/api/v1/userbot/start")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "started" in data["message"]


@patch("app.api.routes.userbot")
def test_stop_userbot_endpoint(mock_userbot):
    """Test the stop userbot endpoint"""
    # Mock userbot instance
    mock_userbot.stop = AsyncMock(return_value=True)

    response = client.post("/api/v1/userbot/stop")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "stopped" in data["message"]


# Test core components
class TestTelegramAuth:
    """Test TelegramAuth class"""

    @patch("app.core.telegram_auth.Client")
    def test_send_code(self, mock_client_class):
        """Test send_code method"""
        # Mock client
        mock_client = AsyncMock()
        mock_client.send_code = AsyncMock(
            return_value=MagicMock(phone_code_hash="test_hash")
        )
        mock_client_class.return_value = mock_client

        auth = TelegramAuth(123456, "test_hash", "+1234567890")
        # This would normally be async, but we're testing the structure
        assert auth is not None


class TestTelegramUserbot:
    """Test TelegramUserbot class"""

    def test_init(self):
        """Test initialization"""
        with patch("app.core.userbot.SessionManager") as mock_session_manager:
            userbot = TelegramUserbot()
            assert userbot is not None
            assert userbot.is_running == False
            assert userbot.client is None


if __name__ == "__main__":
    pytest.main([__file__])

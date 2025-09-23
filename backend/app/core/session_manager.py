"""
Session Management Module
Handles secure storage and management of user sessions
"""

import json
import os
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SessionManager:
    """Manage user sessions and secure storage"""

    def __init__(self, encryption_key: Optional[bytes] = None):
        """
        Initialize session manager

        Args:
            encryption_key: Encryption key for secure storage (optional)
        """
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.session_file = "sessions.json"

    def encrypt_data(self, data: str) -> bytes:
        """
        Encrypt data using Fernet cipher

        Args:
            data: Data to encrypt

        Returns:
            bytes: Encrypted data
        """
        return self.cipher.encrypt(data.encode())

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """
        Decrypt data using Fernet cipher

        Args:
            encrypted_data: Data to decrypt

        Returns:
            str: Decrypted data
        """
        return self.cipher.decrypt(encrypted_data).decode()

    def save_session(self, user_id: str, session_data: Dict[str, Any]) -> bool:
        """
        Save session data securely

        Args:
            user_id: User identifier
            session_data: Session data to save

        Returns:
            bool: True if saved successfully
        """
        try:
            # Load existing sessions
            sessions = self.load_all_sessions()

            # Encrypt sensitive data
            encrypted_session = {}
            for key, value in session_data.items():
                if isinstance(value, str):
                    encrypted_session[key] = self.encrypt_data(value).decode()
                else:
                    encrypted_session[key] = value

            # Save session
            sessions[user_id] = encrypted_session

            # Write to file
            with open(self.session_file, "w") as f:
                json.dump(sessions, f, indent=2)

            logger.info(f"Session saved for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Error saving session: {e}")
            return False

    def load_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Load session data for a user

        Args:
            user_id: User identifier

        Returns:
            dict: Session data or None if not found
        """
        try:
            sessions = self.load_all_sessions()

            if user_id not in sessions:
                return None

            # Decrypt sensitive data
            encrypted_session = sessions[user_id]
            session_data = {}

            for key, value in encrypted_session.items():
                try:
                    # Try to decrypt, if it's encrypted
                    if isinstance(value, str):
                        session_data[key] = self.decrypt_data(value.encode())
                    else:
                        session_data[key] = value
                except Exception:
                    # If decryption fails, keep original value
                    session_data[key] = value

            return session_data

        except Exception as e:
            logger.error(f"Error loading session: {e}")
            return None

    def load_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all sessions from storage

        Returns:
            dict: All sessions
        """
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading sessions: {e}")
            return {}

    def delete_session(self, user_id: str) -> bool:
        """
        Delete a user session

        Args:
            user_id: User identifier

        Returns:
            bool: True if deleted successfully
        """
        try:
            sessions = self.load_all_sessions()

            if user_id in sessions:
                del sessions[user_id]

                # Write updated sessions to file
                with open(self.session_file, "w") as f:
                    json.dump(sessions, f, indent=2)

                logger.info(f"Session deleted for user {user_id}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            return False

    def get_encryption_key(self) -> bytes:
        """
        Get the encryption key (for secure storage)

        Returns:
            bytes: Encryption key
        """
        return self.encryption_key

"""
Telegram Authentication Module
Handles user authentication with Telegram MTProto API using PyroFork
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from pyrogram import Client
from pyrogram.errors import (
    PhoneCodeInvalid, 
    PhoneCodeExpired, 
    SessionPasswordNeeded,
    PasswordHashInvalid,
    FloodWait
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramAuth:
    """Handle Telegram user authentication"""
    
    def __init__(self, api_id: int, api_hash: str, phone_number: str):
        """
        Initialize Telegram authentication
        
        Args:
            api_id: Telegram API ID
            api_hash: Telegram API Hash
            phone_number: User's phone number
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client: Optional[Client] = None
        self.session_string: Optional[str] = None
    
    async def send_code(self) -> str:
        """
        Send authentication code to user's phone number
        
        Returns:
            str: Phone code hash
        """
        try:
            self.client = Client(
                "telegram_userbot",
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone_number=self.phone_number
            )
            
            # Send code request
            sent_code = await self.client.send_code(self.phone_number)
            logger.info("Authentication code sent successfully")
            return sent_code.phone_code_hash
            
        except FloodWait as e:
            logger.error(f"Flood wait for {e.value} seconds")
            raise
        except Exception as e:
            logger.error(f"Error sending code: {e}")
            raise
    
    async def sign_in(self, code: str, phone_code_hash: str) -> bool:
        """
        Sign in with received code
        
        Args:
            code: Received code from Telegram
            phone_code_hash: Phone code hash from send_code
            
        Returns:
            bool: True if sign in successful
        """
        try:
            if not self.client:
                raise Exception("Client not initialized")
                
            # Sign in with code
            await self.client.sign_in(
                phone_number=self.phone_number,
                phone_code_hash=phone_code_hash,
                phone_code=code
            )
            
            # Save session string
            self.session_string = await self.client.export_session_string()
            logger.info("Sign in successful")
            return True
            
        except PhoneCodeInvalid:
            logger.error("Invalid phone code")
            raise
        except PhoneCodeExpired:
            logger.error("Phone code expired")
            raise
        except Exception as e:
            logger.error(f"Error signing in: {e}")
            raise
    
    async def sign_in_with_password(self, password: str) -> bool:
        """
        Sign in with password for 2FA enabled accounts
        
        Args:
            password: User's 2FA password
            
        Returns:
            bool: True if sign in successful
        """
        try:
            if not self.client:
                raise Exception("Client not initialized")
                
            # Sign in with password
            await self.client.check_password(password)
            
            # Save session string
            self.session_string = await self.client.export_session_string()
            logger.info("Sign in with password successful")
            return True
            
        except PasswordHashInvalid:
            logger.error("Invalid password")
            raise
        except Exception as e:
            logger.error(f"Error signing in with password: {e}")
            raise
    
    async def start_client(self) -> bool:
        """
        Start the Telegram client with existing session
        
        Returns:
            bool: True if client started successfully
        """
        try:
            if not self.client:
                if not self.session_string:
                    raise Exception("No session string available")
                
                # Initialize client with session string
                self.client = Client(
                    "telegram_userbot",
                    api_id=self.api_id,
                    api_hash=self.api_hash,
                    session_string=self.session_string
                )
            
            # Start the client
            await self.client.start()
            logger.info("Telegram client started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error starting client: {e}")
            raise
    
    async def stop_client(self) -> bool:
        """
        Stop the Telegram client
        
        Returns:
            bool: True if client stopped successfully
        """
        try:
            if self.client and self.client.is_connected:
                await self.client.stop()
                logger.info("Telegram client stopped successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Error stopping client: {e}")
            raise
    
    def get_session_string(self) -> Optional[str]:
        """
        Get the session string for persistent login
        
        Returns:
            str: Session string or None if not available
        """
        return self.session_string
    
    async def get_me(self) -> Optional[Dict[str, Any]]:
        """
        Get current user information
        
        Returns:
            dict: User information or None if not available
        """
        try:
            if not self.client or not self.client.is_connected:
                await self.start_client()
            
            me = await self.client.get_me()
            return {
                "id": me.id,
                "username": me.username,
                "first_name": me.first_name,
                "last_name": me.last_name,
                "phone_number": me.phone_number
            }
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return None



"""
Telegram Userbot Core
Main implementation of the Telegram userbot functionality
"""

import asyncio
import logging
from typing import Optional, List, Dict, Any
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import (
    FloodWait,
    ChatWriteForbidden,
    ChatForbidden,
    ChatIdInvalid,
    UserBlocked,
    PeerIdInvalid,
    ChannelInvalid,
    UserBannedInChannel,
    ChatRestricted,
    SlowmodeWait,
)
import time
import random
from datetime import datetime, timedelta
from .telegram_auth import TelegramAuth
from .config import settings
from .session_manager import SessionManager
from .repository import (
    GroupRepository,
    MessageRepository,
    BlacklistRepository,
    ConfigRepository,
)
from .database import get_db_session

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramUserbot:
    """Main Telegram userbot class"""

    def __init__(self):
        """Initialize the userbot"""
        self.client: Optional[Client] = None
        self.auth: Optional[TelegramAuth] = None
        self.session_manager = SessionManager()
        self.is_running = False
        self.db = get_db_session()
        self.group_repo = GroupRepository(self.db)
        self.message_repo = MessageRepository(self.db)
        self.blacklist_repo = BlacklistRepository(self.db)
        self.config_repo = ConfigRepository(self.db)
        self.config = {
            "message_interval": (5, 10),  # 5-10 seconds between messages
            "cycle_interval": (4200, 4680),  # 1.1-1.3 hours between cycles (in seconds)
        }

    async def initialize(self) -> bool:
        """
        Initialize the userbot with existing session or new authentication

        Returns:
            bool: True if initialization successful
        """
        try:
            # Check if we have a session string
            session_data = self.session_manager.load_session("default")

            if session_data and session_data.get("session_string"):
                # Use existing session
                self.auth = TelegramAuth(
                    settings.telegram_api_id,
                    settings.telegram_api_hash,
                    session_data.get("phone_number", ""),
                )
                self.auth.session_string = session_data["session_string"]
                await self.auth.start_client()
                self.client = self.auth.client
            else:
                # Need to authenticate
                if not settings.phone_number:
                    raise Exception("Phone number required for initial authentication")

                self.auth = TelegramAuth(
                    settings.telegram_api_id,
                    settings.telegram_api_hash,
                    settings.phone_number,
                )

            # Set up client event handlers
            if self.client:
                self._setup_event_handlers()

            # Load configuration from database
            self._load_config_from_db()

            logger.info("Userbot initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Error initializing userbot: {e}")
            raise

    def _setup_event_handlers(self):
        """Set up event handlers for the client"""
        if not self.client:
            return

        @self.client.on_message(filters.command("ping", prefixes=".") & filters.me)
        async def ping_handler(client: Client, message: Message):
            """Handle ping command"""
            await message.edit("Pong!")

        @self.client.on_message(filters.command("help", prefixes=".") & filters.me)
        async def help_handler(client: Client, message: Message):
            """Handle help command"""
            help_text = """
Telegram Userbot Commands:
.ping - Check if userbot is running
.help - Show this help message
.status - Show userbot status
.groups - Show managed groups
"""
            await message.edit(help_text)

    def _load_config_from_db(self):
        """Load configuration from database"""
        try:
            # Ensure default configurations exist
            message_interval_cfg = self.config_repo.get_config_by_key(
                "message_interval"
            )
            if not message_interval_cfg:
                self.config_repo.set_config(
                    "message_interval",
                    "5-10",
                    "Delay between messages (min-max seconds)",
                )

            cycle_interval_cfg = self.config_repo.get_config_by_key("cycle_interval")
            if not cycle_interval_cfg:
                self.config_repo.set_config(
                    "cycle_interval",
                    "4200-4680",
                    "Delay between cycles (min-max seconds)",
                )

            # Load message interval
            message_interval = self.config_repo.get_config_value(
                "message_interval", "5-10"
            )
            try:
                min_val, max_val = map(int, message_interval.split("-"))
                self.config["message_interval"] = (min_val, max_val)
            except:
                self.config["message_interval"] = (5, 10)

            # Load cycle interval
            cycle_interval = self.config_repo.get_config_value(
                "cycle_interval", "4200-4680"
            )
            try:
                min_val, max_val = map(int, cycle_interval.split("-"))
                self.config["cycle_interval"] = (min_val, max_val)
            except:
                self.config["cycle_interval"] = (4200, 4680)
        except Exception as e:
            logger.error(f"Error loading configuration from database: {e}")
            # Use default values
            self.config["message_interval"] = (5, 10)
            self.config["cycle_interval"] = (4200, 4680)

    async def start(self) -> bool:
        """
        Start the userbot

        Returns:
            bool: True if started successfully
        """
        try:
            if not self.client:
                await self.initialize()

            if not self.client.is_connected:
                await self.client.start()

            self.is_running = True
            logger.info("Userbot started successfully")
            return True

        except Exception as e:
            logger.error(f"Error starting userbot: {e}")
            raise

    async def stop(self) -> bool:
        """
        Stop the userbot

        Returns:
            bool: True if stopped successfully
        """
        try:
            self.is_running = False

            if self.client and self.client.is_connected:
                await self.client.stop()

            # Close database session
            self.db.close()

            logger.info("Userbot stopped successfully")
            return True

        except Exception as e:
            logger.error(f"Error stopping userbot: {e}")
            raise

    async def authenticate_new_session(self, code: str, phone_code_hash: str) -> bool:
        """
        Authenticate with a new session using received code

        Args:
            code: Received code from Telegram
            phone_code_hash: Phone code hash

        Returns:
            bool: True if authentication successful
        """
        try:
            if not self.auth:
                raise Exception("Authentication module not initialized")

            # Sign in with code
            await self.auth.sign_in(code, phone_code_hash)

            # Save session
            session_data = {
                "api_id": settings.telegram_api_id,
                "api_hash": settings.telegram_api_hash,
                "phone_number": settings.phone_number,
                "session_string": self.auth.get_session_string(),
            }
            self.session_manager.save_session("default", session_data)

            # Start client
            await self.auth.start_client()
            self.client = self.auth.client

            # Set up event handlers
            self._setup_event_handlers()

            logger.info("New session authenticated successfully")
            return True

        except Exception as e:
            logger.error(f"Error authenticating new session: {e}")
            raise

    async def authenticate_with_password(self, password: str) -> bool:
        """
        Authenticate with password for 2FA enabled accounts

        Args:
            password: 2FA password

        Returns:
            bool: True if authentication successful
        """
        try:
            if not self.auth:
                raise Exception("Authentication module not initialized")

            # Sign in with password
            await self.auth.sign_in_with_password(password)

            # Save session
            session_data = {
                "api_id": settings.telegram_api_id,
                "api_hash": settings.telegram_api_hash,
                "phone_number": settings.phone_number,
                "session_string": self.auth.get_session_string(),
            }
            self.session_manager.save_session("default", session_data)

            # Start client
            await self.auth.start_client()
            self.client = self.auth.client

            # Set up event handlers
            self._setup_event_handlers()

            logger.info("Authenticated with password successfully")
            return True

        except Exception as e:
            logger.error(f"Error authenticating with password: {e}")
            raise

    def add_group(self, group_identifier: str) -> bool:
        """
        Add a group to the managed list

        Args:
            group_identifier: Group link, username, or ID

        Returns:
            bool: True if added successfully
        """
        try:
            # Check if group already exists
            existing_group = self.group_repo.get_group_by_identifier(group_identifier)
            if not existing_group:
                self.group_repo.create_group(group_identifier)
                logger.info(f"Group {group_identifier} added to managed list")
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding group: {e}")
            return False

    def remove_group(self, group_identifier: str) -> bool:
        """
        Remove a group from the managed list

        Args:
            group_identifier: Group link, username, or ID

        Returns:
            bool: True if removed successfully
        """
        try:
            group = self.group_repo.get_group_by_identifier(group_identifier)
            if group:
                self.group_repo.delete_group(group.id)
                logger.info(f"Group {group_identifier} removed from managed list")
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing group: {e}")
            return False

    def add_message(self, message_text: str) -> bool:
        """
        Add a message to the message queue

        Args:
            message_text: Text of the message to send

        Returns:
            bool: True if added successfully
        """
        try:
            self.message_repo.create_message(message_text)
            logger.info(f"Message added to queue: {message_text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Error adding message: {e}")
            return False

    def remove_message(self, message_id: int) -> bool:
        """
        Remove a message from the message queue

        Args:
            message_id: ID of the message to remove

        Returns:
            bool: True if removed successfully
        """
        try:
            result = self.message_repo.delete_message(message_id)
            if result:
                logger.info(f"Message {message_id} removed from queue")
            return result
        except Exception as e:
            logger.error(f"Error removing message: {e}")
            return False

    def update_config(self, config_key: str, config_value: Any) -> bool:
        """
        Update configuration settings

        Args:
            config_key: Configuration key to update
            config_value: New value for the configuration

        Returns:
            bool: True if updated successfully
        """
        try:
            # Update in database
            self.config_repo.set_config(config_key, str(config_value))

            # Update in memory
            if config_key in ["message_interval", "cycle_interval"]:
                try:
                    min_val, max_val = map(int, str(config_value).split("-"))
                    self.config[config_key] = (min_val, max_val)
                except:
                    logger.error(f"Invalid format for {config_key}: {config_value}")
                    return False
            else:
                self.config[config_key] = config_value

            logger.info(f"Configuration updated: {config_key} = {config_value}")
            return True
        except Exception as e:
            logger.error(f"Error updating configuration: {e}")
            return False

    def add_to_blacklist(
        self, chat_id: str, reason: str, duration: Optional[int] = None
    ) -> bool:
        """
        Add a chat to the blacklist

        Args:
            chat_id: Chat ID to blacklist
            reason: Reason for blacklisting
            duration: Duration in seconds for temporary blacklist (None for permanent)

        Returns:
            bool: True if added successfully
        """
        try:
            if duration:
                # Temporary blacklist
                expiry_time = datetime.utcnow() + timedelta(seconds=duration)
                self.blacklist_repo.add_to_blacklist(
                    chat_id, reason, False, expiry_time
                )
                logger.info(
                    f"Chat {chat_id} temporarily blacklisted for {duration} seconds: {reason}"
                )
            else:
                # Permanent blacklist
                self.blacklist_repo.add_to_blacklist(chat_id, reason, True)
                logger.info(f"Chat {chat_id} permanently blacklisted: {reason}")

            return True
        except Exception as e:
            logger.error(f"Error adding to blacklist: {e}")
            return False

    def remove_from_blacklist(self, chat_id: str) -> bool:
        """
        Remove a chat from the blacklist

        Args:
            chat_id: Chat ID to remove from blacklist

        Returns:
            bool: True if removed successfully
        """
        try:
            result = self.blacklist_repo.remove_from_blacklist(chat_id)
            if result:
                logger.info(f"Chat {chat_id} removed from blacklist")
            return result
        except Exception as e:
            logger.error(f"Error removing from blacklist: {e}")
            return False

    def clean_temporary_blacklist(self) -> int:
        """
        Clean expired temporary blacklist entries

        Returns:
            int: Number of entries cleaned
        """
        try:
            cleaned_count = self.blacklist_repo.clean_expired_blacklist()
            if cleaned_count > 0:
                logger.info(f"Cleaned {cleaned_count} expired blacklist entries")
            return cleaned_count
        except Exception as e:
            logger.error(f"Error cleaning temporary blacklist: {e}")
            return 0

    def is_blacklisted(self, chat_id: str) -> bool:
        """
        Check if a chat is blacklisted

        Args:
            chat_id: Chat ID to check

        Returns:
            bool: True if blacklisted
        """
        try:
            return self.blacklist_repo.is_blacklisted(chat_id)
        except Exception as e:
            logger.error(f"Error checking blacklist status: {e}")
            return False

    async def send_messages_to_groups(self) -> bool:
        """
        Send messages to all managed groups

        Returns:
            bool: True if messages sent successfully
        """
        try:
            if not self.client or not self.client.is_connected:
                raise Exception("Client not connected")

            # Get all active messages
            messages = self.message_repo.get_all_messages()
            if not messages:
                logger.info("No messages to send")
                return True

            # Get all active groups
            groups = self.group_repo.get_all_groups()
            if not groups:
                logger.info("No groups to send messages to")
                return True

            # Clean temporary blacklist
            self.clean_temporary_blacklist()

            # Send messages to each group
            for group in groups:
                if not self.is_running:
                    break

                # Skip blacklisted groups
                if self.is_blacklisted(group.identifier):
                    logger.info(f"Skipping blacklisted group: {group.identifier}")
                    continue

                # Send each message to the group
                for message in messages:
                    if not self.is_running:
                        break

                    try:
                        # Send message
                        await self.client.send_message(group.identifier, message.text)
                        logger.info(
                            f"Message sent to {group.identifier}: {message.text[:50]}..."
                        )

                        # Wait for random interval between messages
                        interval = random.randint(*self.config["message_interval"])
                        await asyncio.sleep(interval)

                    except (
                        ChatWriteForbidden,
                        ChatForbidden,
                        ChatIdInvalid,
                        UserBlocked,
                        PeerIdInvalid,
                        ChannelInvalid,
                        UserBannedInChannel,
                        ChatRestricted,
                    ) as e:
                        logger.warning(
                            f"Chat error for {group.identifier}: {type(e).__name__}, adding to permanent blacklist"
                        )
                        self.add_to_blacklist(group.identifier, type(e).__name__)
                        break
                    except SlowmodeWait as e:
                        logger.warning(
                            f"Slow mode wait for {e.value} seconds for {group.identifier}"
                        )
                        self.add_to_blacklist(group.identifier, "SlowmodeWait", e.value)
                        await asyncio.sleep(e.value)
                    except FloodWait as e:
                        logger.warning(
                            f"Flood wait for {e.value} seconds for {group.identifier}"
                        )
                        self.add_to_blacklist(group.identifier, "FloodWait", e.value)
                        await asyncio.sleep(e.value)
                    except Exception as e:
                        logger.error(
                            f"Error sending message to {group.identifier}: {e}"
                        )
                        # Add to permanent blacklist for other errors
                        self.add_to_blacklist(
                            group.identifier, f"UnknownError: {str(e)}"
                        )
                        break

                # Wait for random interval between groups
                if self.is_running and group != groups[-1]:
                    interval = random.randint(*self.config["message_interval"])
                    await asyncio.sleep(interval)

            return True

        except Exception as e:
            logger.error(f"Error sending messages to groups: {e}")
            raise

    async def run_automatic_posting_cycle(self) -> bool:
        """
        Run one complete automatic posting cycle

        Returns:
            bool: True if cycle completed successfully
        """
        try:
            logger.info("Starting automatic posting cycle")

            # Clean temporary blacklist at the beginning of each cycle
            self.clean_temporary_blacklist()

            # Send messages
            await self.send_messages_to_groups()

            logger.info("Automatic posting cycle completed")
            return True

        except Exception as e:
            logger.error(f"Error in automatic posting cycle: {e}")
            raise

    async def run_continuous_posting(self) -> None:
        """Run continuous automatic posting cycles"""
        try:
            while self.is_running:
                # Run one cycle
                await self.run_automatic_posting_cycle()

                # Wait for random interval between cycles
                interval = random.randint(*self.config["cycle_interval"])
                logger.info(f"Waiting {interval} seconds before next cycle")

                # Wait in small intervals to allow for graceful shutdown
                for _ in range(interval // 10):
                    if not self.is_running:
                        break
                    await asyncio.sleep(10)

                if not self.is_running:
                    break

        except Exception as e:
            logger.error(f"Error in continuous posting: {e}")
            raise

"""
API Routes Module
Contains all API routes for the Telegram Userbot TMA
"""

from fastapi import APIRouter, HTTPException, Request
from typing import List, Optional
from pydantic import BaseModel, field_validator
from ..core.userbot import TelegramUserbot
from ..core.api_error_handler import handle_api_errors
from ..core.rate_limiter import limiter, DEFAULT_LIMIT

# Create router
router = APIRouter()

# Global userbot instance (in a real implementation, this would be dependency injected)
userbot: Optional[TelegramUserbot] = None


# Pydantic models for request/response
class AuthRequest(BaseModel):
    code: str
    phone_code_hash: str


class PasswordAuthRequest(BaseModel):
    password: str


class GroupRequest(BaseModel):
    identifier: str

    @field_validator('identifier')
    @classmethod
    def validate_group_identifier(cls, v):
        if len(v) > 255:
            raise ValueError('Group identifier must be at most 255 characters')
        # Basic validation for group identifier format
        if not (v.startswith('https://t.me/') or v.startswith('@') or v.lstrip('-').isdigit()):
            raise ValueError('Group identifier must be a valid group link, username, or ID')
        return v


class BulkGroupsRequest(BaseModel):
    identifiers: List[str]

    @field_validator('identifiers')
    @classmethod
    def validate_group_identifiers(cls, v):
        if len(v) > 100:  # Limit bulk operations
            raise ValueError('Cannot add more than 100 groups at once')
        for identifier in v:
            if len(identifier) > 255:
                raise ValueError('Each group identifier must be at most 255 characters')
            if not (identifier.startswith('https://t.me/') or identifier.startswith('@') or identifier.lstrip('-').isdigit()):
                raise ValueError('Each group identifier must be a valid group link, username, or ID')
        return v


class MessageRequest(BaseModel):
    text: str

    @field_validator('text')
    @classmethod
    def validate_message_text(cls, v):
        if not v or len(v) > 4096:  # Telegram message limit is 4096 characters
            raise ValueError('Message text must be between 1 and 4096 characters')
        
        # Check for potential harmful content
        import re
        harmful_patterns = [
            r'<script',  # Potential XSS
            r'javascript:',  # Potential XSS
            r'on\w+\s*=',  # Potential event handlers
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Message contains potentially harmful content')
        
        return v


class ConfigRequest(BaseModel):
    key: str
    value: str

    @field_validator('key')
    @classmethod
    def validate_config_key(cls, v):
        if not v or len(v) > 100:
            raise ValueError('Config key must be between 1 and 100 characters')
        # Only allow alphanumeric, underscore, and hyphen
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Config key can only contain letters, numbers, underscores, and hyphens')
        return v

    @field_validator('value')
    @classmethod
    def validate_config_value(cls, v):
        if len(v) > 1000:
            raise ValueError('Config value must be at most 1000 characters')
        return v


class BlacklistRequest(BaseModel):
    chat_id: str
    reason: str
    duration: Optional[int] = None

    @field_validator('chat_id')
    @classmethod
    def validate_chat_id(cls, v):
        if not v or len(v) > 50:
            raise ValueError('Chat ID must be between 1 and 50 characters')
        # Should be a valid number for chat ID
        try:
            int(v.lstrip('-'))  # Telegram chat IDs can be negative (for supergroups)
        except ValueError:
            raise ValueError('Chat ID must be a valid integer (with optional negative sign)')
        return v

    @field_validator('reason')
    @classmethod
    def validate_reason(cls, v):
        if not v or len(v) > 500:
            raise ValueError('Reason must be between 1 and 500 characters')
        return v

    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Duration must be a positive integer if provided')
        if v and v > 31536000:  # 1 year in seconds
            raise ValueError('Duration cannot be more than 1 year')
        return v


# Initialize userbot on startup
async def initialize_userbot():
    """Initialize userbot"""
    global userbot
    userbot = TelegramUserbot()
    try:
        await userbot.initialize()
        print("Userbot initialized successfully")
    except Exception as e:
        print(f"Error initializing userbot: {e}")


# Clean up on shutdown
async def cleanup_userbot():
    """Clean up userbot"""
    global userbot
    if userbot:
        await userbot.stop()


# Authentication endpoints
@router.post("/auth/send-code")
@limiter.limit("5/minute")  # More restrictive for auth endpoints
@handle_api_errors
async def send_auth_code(request: Request):  # Note: request parameter is needed for limiter
    """Send authentication code to user's phone"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    if not userbot.auth:
        raise HTTPException(status_code=500, detail="Userbot authentication not initialized")

    phone_code_hash = await userbot.auth.send_code()
    return {"phone_code_hash": phone_code_hash}


@router.post("/auth/sign-in")
@limiter.limit("10/minute")  # More restrictive for auth endpoints
@handle_api_errors
async def sign_in(request: Request, auth_request: AuthRequest):  # Note: request parameter is needed for limiter
    """Sign in with received code"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    await userbot.authenticate_new_session(
        auth_request.code, auth_request.phone_code_hash
    )
    return {"message": "Authentication successful"}


@router.post("/auth/sign-in-password")
@limiter.limit("10/minute")  # More restrictive for auth endpoints
async def sign_in_password(request: Request, password_request: PasswordAuthRequest):  # Note: request parameter is needed for limiter
    """Sign in with password for 2FA enabled accounts"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        await userbot.authenticate_with_password(password_request.password)
        return {"message": "Authentication with password successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Userbot control endpoints
@router.post("/userbot/start")
@limiter.limit(DEFAULT_LIMIT)
async def start_userbot(request: Request):
    """Start the userbot"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        await userbot.start()
        return {"message": "Userbot started successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/userbot/stop")
@limiter.limit(DEFAULT_LIMIT)
async def stop_userbot(request: Request):
    """Stop the userbot"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        await userbot.stop()
        return {"message": "Userbot stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/userbot/status")
@limiter.limit(DEFAULT_LIMIT)
@handle_api_errors
async def get_userbot_status(request: Request):
    """Get userbot status"""
    global userbot
    if not userbot:
        return {"running": False, "message": "Userbot not initialized"}

    user_info = await userbot.auth.get_me() if userbot.auth else None
    return {
        "running": userbot.is_running,
        "user_info": user_info,
        "message": (
            "Userbot is running" if userbot.is_running else "Userbot is stopped"
        ),
    }


# Group management endpoints
@router.post("/groups")
@limiter.limit(DEFAULT_LIMIT)
@handle_api_errors
async def add_group(request: Request, group_request: GroupRequest):
    """Add a group to managed list"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    result = userbot.add_group(group_request.identifier)
    message_text = "Group added successfully" if result else "Group already exists"
    return {"message": message_text}


@router.post("/groups/bulk")
@limiter.limit("20/minute")  # Limit bulk operations
async def add_groups_bulk(request, bulk_request: BulkGroupsRequest):
    """Add multiple groups to managed list"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        for identifier in bulk_request.identifiers:
            userbot.add_group(identifier)
        return {"message": f"Added {len(bulk_request.identifiers)} groups"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/groups/{identifier}")
@limiter.limit(DEFAULT_LIMIT)
async def remove_group(request, identifier: str):
    """Remove a group from managed list"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        result = userbot.remove_group(identifier)
        message_text = "Group removed successfully" if result else "Group not found"
        return {"message": message_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/groups")
@limiter.limit(DEFAULT_LIMIT)
async def get_groups(request):
    """Get all managed groups"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        groups = userbot.group_repo.get_all_groups()
        return {
            "groups": [
                {"id": g.id, "identifier": g.identifier, "name": g.name} for g in groups
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Message management endpoints
@router.post("/messages")
@limiter.limit(DEFAULT_LIMIT)
async def add_message(request: Request, message_request: MessageRequest):
    """Add a message to the queue"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        result = userbot.add_message(message_request.text)
        return {
            "message": (
                "Message added successfully" if result else "Failed to add message"
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/messages/{message_id}")
@limiter.limit(DEFAULT_LIMIT)
async def remove_message(request, message_id: int):
    """Remove a message from the queue"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        result = userbot.remove_message(message_id)
        message_text = "Message removed successfully" if result else "Message not found"
        return {"message": message_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/messages")
@limiter.limit(DEFAULT_LIMIT)
async def get_messages(request):
    """Get all messages in the queue"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        messages = userbot.message_repo.get_all_messages()
        return {"messages": [{"id": m.id, "text": m.text} for m in messages]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Configuration endpoints
@router.post("/config")
@limiter.limit(DEFAULT_LIMIT)
async def update_config(request: Request, config_request: ConfigRequest):
    """Update configuration settings"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        result = userbot.update_config(config_request.key, config_request.value)
        return {
            "message": (
                "Configuration updated successfully"
                if result
                else "Failed to update configuration"
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/config")
@limiter.limit(DEFAULT_LIMIT)
async def get_config(request):
    """Get all configuration settings"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        configs = userbot.config_repo.get_all_configs()
        return {
            "config": [
                {"key": c.key, "value": c.value, "description": c.description}
                for c in configs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Blacklist management endpoints
@router.post("/blacklist")
@limiter.limit(DEFAULT_LIMIT)
async def add_to_blacklist(request: Request, blacklist_request: BlacklistRequest):
    """Add a chat to blacklist"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        result = userbot.add_to_blacklist(
            blacklist_request.chat_id,
            blacklist_request.reason,
            blacklist_request.duration,
        )
        return {
            "message": (
                "Chat added to blacklist successfully"
                if result
                else "Failed to add chat to blacklist"
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/blacklist/{chat_id}")
@limiter.limit(DEFAULT_LIMIT)
async def remove_from_blacklist(request: Request, chat_id: str):
    """Remove a chat from blacklist"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        result = userbot.remove_from_blacklist(chat_id)
        return {
            "message": (
                "Chat removed from blacklist successfully"
                if result
                else "Chat not found in blacklist"
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/blacklist")
@limiter.limit(DEFAULT_LIMIT)
async def get_blacklist(request):
    """Get all blacklisted chats"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")

    try:
        blacklisted_chats = userbot.blacklist_repo.get_all_blacklisted_chats()
        return {
            "blacklisted_chats": [
                {
                    "id": b.id,
                    "chat_id": b.chat_id,
                    "reason": b.reason,
                    "is_permanent": b.is_permanent,
                    "expiry_time": b.expiry_time.isoformat() if b.expiry_time else None,
                }
                for b in blacklisted_chats
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
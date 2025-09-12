"""
API Routes Module
Contains all API routes for the Telegram Userbot TMA
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import asyncio
from ..core.userbot import TelegramUserbot
from ..core.config import settings

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


class BulkGroupsRequest(BaseModel):
    identifiers: List[str]


class MessageRequest(BaseModel):
    text: str


class ConfigRequest(BaseModel):
    key: str
    value: str


class BlacklistRequest(BaseModel):
    chat_id: str
    reason: str
    duration: Optional[int] = None


# Initialize userbot on startup
@router.on_event("startup")
async def startup_event():
    """Initialize userbot on startup"""
    global userbot
    userbot = TelegramUserbot()
    try:
        await userbot.initialize()
        print("Userbot initialized successfully")
    except Exception as e:
        print(f"Error initializing userbot: {e}")


# Clean up on shutdown
@router.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    global userbot
    if userbot:
        await userbot.stop()


# Authentication endpoints
@router.post("/auth/send-code")
async def send_auth_code():
    """Send authentication code to user's phone"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        phone_code_hash = await userbot.auth.send_code()
        return {"phone_code_hash": phone_code_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/sign-in")
async def sign_in(auth_request: AuthRequest):
    """Sign in with received code"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        await userbot.authenticate_new_session(auth_request.code, auth_request.phone_code_hash)
        return {"message": "Authentication successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/sign-in-password")
async def sign_in_password(password_request: PasswordAuthRequest):
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
async def start_userbot():
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
async def stop_userbot():
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
async def get_userbot_status():
    """Get userbot status"""
    global userbot
    if not userbot:
        return {"running": False, "message": "Userbot not initialized"}
    
    try:
        user_info = await userbot.auth.get_me() if userbot.auth else None
        return {
            "running": userbot.is_running,
            "user_info": user_info,
            "message": "Userbot is running" if userbot.is_running else "Userbot is stopped"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Group management endpoints
@router.post("/groups")
async def add_group(group_request: GroupRequest):
    """Add a group to managed list"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        result = userbot.add_group(group_request.identifier)
        return {"message": "Group added successfully" if result else "Group already exists"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/groups/bulk")
async def add_groups_bulk(bulk_request: BulkGroupsRequest):
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
async def remove_group(identifier: str):
    """Remove a group from managed list"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        result = userbot.remove_group(identifier)
        return {"message": "Group removed successfully" if result else "Group not found"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/groups")
async def get_groups():
    """Get all managed groups"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        from ..core.repository import GroupRepository
        repo = GroupRepository()
        groups = repo.get_all_groups()
        return {"groups": [{"id": g.id, "identifier": g.identifier, "name": g.name} for g in groups]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Message management endpoints
@router.post("/messages")
async def add_message(message_request: MessageRequest):
    """Add a message to the queue"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        result = userbot.add_message(message_request.text)
        return {"message": "Message added successfully" if result else "Failed to add message"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/messages/{message_id}")
async def remove_message(message_id: int):
    """Remove a message from the queue"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        result = userbot.remove_message(message_id)
        return {"message": "Message removed successfully" if result else "Message not found"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/messages")
async def get_messages():
    """Get all messages in the queue"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        from ..core.repository import MessageRepository
        repo = MessageRepository()
        messages = repo.get_all_messages()
        return {"messages": [{"id": m.id, "text": m.text} for m in messages]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Configuration endpoints
@router.post("/config")
async def update_config(config_request: ConfigRequest):
    """Update configuration settings"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        result = userbot.update_config(config_request.key, config_request.value)
        return {"message": "Configuration updated successfully" if result else "Failed to update configuration"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/config")
async def get_config():
    """Get all configuration settings"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        from ..core.repository import ConfigRepository
        repo = ConfigRepository()
        configs = repo.get_all_configs()
        return {"config": [{"key": c.key, "value": c.value, "description": c.description} for c in configs]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Blacklist management endpoints
@router.post("/blacklist")
async def add_to_blacklist(blacklist_request: BlacklistRequest):
    """Add a chat to blacklist"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        result = userbot.add_to_blacklist(
            blacklist_request.chat_id, 
            blacklist_request.reason, 
            blacklist_request.duration
        )
        return {"message": "Chat added to blacklist successfully" if result else "Failed to add chat to blacklist"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/blacklist/{chat_id}")
async def remove_from_blacklist(chat_id: str):
    """Remove a chat from blacklist"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        result = userbot.remove_from_blacklist(chat_id)
        return {"message": "Chat removed from blacklist successfully" if result else "Chat not found in blacklist"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/blacklist")
async def get_blacklist():
    """Get all blacklisted chats"""
    global userbot
    if not userbot:
        raise HTTPException(status_code=500, detail="Userbot not initialized")
    
    try:
        from ..core.repository import BlacklistRepository
        repo = BlacklistRepository()
        blacklisted_chats = repo.get_all_blacklisted_chats()
        return {
            "blacklisted_chats": [
                {
                    "id": b.id, 
                    "chat_id": b.chat_id, 
                    "reason": b.reason, 
                    "is_permanent": b.is_permanent,
                    "expiry_time": b.expiry_time.isoformat() if b.expiry_time else None
                } 
                for b in blacklisted_chats
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
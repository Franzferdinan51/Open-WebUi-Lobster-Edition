"""
OpenClaw Control Panel - Channels Router
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.models.users import User

from open_webui.plugins.openclaw_control import get_control_client, OpenClawControlClient

log = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/openclaw/channels")
async def list_channels(user: User = Depends(get_verified_user)):
    """List all OpenClaw channels"""
    client = get_control_client()
    channels = client.get_channels()
    return {"object": "list", "data": channels}


@router.get("/api/openclaw/channels/{channel_id}")
async def get_channel(channel_id: str, user: User = Depends(get_verified_user)):
    """Get specific channel"""
    client = get_control_client()
    channel = client.get_channel(channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel


@router.put("/api/openclaw/channels/{channel_id}")
async def update_channel(channel_id: str, config: Dict[Any, Any], user: User = Depends(get_admin_user)):
    """Update channel configuration"""
    client = get_control_client()
    result = client.update_channel(channel_id, config)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/api/openclaw/channels/types")
async def channel_types(user: User = Depends(get_verified_user)):
    """Get available channel types"""
    return {
        "types": [
            {"id": "telegram", "name": "Telegram", "icon": "telegram"},
            {"id": "whatsapp", "name": "WhatsApp", "icon": "whatsapp"},
            {"id": "discord", "name": "Discord", "icon": "discord"},
            {"id": "slack", "name": "Slack", "icon": "slack"},
            {"id": "signal", "name": "Signal", "icon": "signal"},
            {"id": "imessage", "name": "iMessage", "icon": "imessage"},
            {"id": "googlechat", "name": "Google Chat", "icon": "google"},
        ]
    }

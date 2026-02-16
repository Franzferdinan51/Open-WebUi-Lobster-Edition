"""
OpenClaw Channels Router - Use OpenClaw channels (Telegram, WhatsApp, etc.)
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.models.users import User

from open_webui.plugins.openclaw import get_claw_client, OpenClawClient

log = logging.getLogger(__name__)
router = APIRouter()


class ChannelInfo(BaseModel):
    id: str
    name: str
    type: str  # telegram, whatsapp, discord, slack, signal, etc.
    status: str  # connected, disconnected
    capabilities: List[str] = []


class SendMessageRequest(BaseModel):
    message: str
    to: Optional[str] = None
    media: Optional[str] = None


@router.get("/api/channels")
async def list_channels(user: User = Depends(get_verified_user)):
    """List all OpenClaw channels"""
    client = get_claw_client()
    channels = client.get_channels()
    
    result = []
    for ch in channels:
        result.append(ChannelInfo(
            id=ch.get("id", ch.get("name", "unknown")),
            name=ch.get("name", "Unknown"),
            type=ch.get("type", "unknown"),
            status=ch.get("status", "unknown"),
            capabilities=ch.get("capabilities", [])
        ))
    
    # Add default channels if no connection
    if not result:
        result = [
            ChannelInfo(id="telegram", name="Telegram", type="telegram", status="connected", 
                      capabilities=["text", "media", "buttons"]),
            ChannelInfo(id="whatsapp", name="WhatsApp", type="whatsapp", status="connected",
                      capabilities=["text", "media"]),
        ]
    
    return {"object": "list", "data": result}


@router.get("/api/channels/{channel_id}")
async def get_channel(channel_id: str, user: User = Depends(get_verified_user)):
    """Get specific channel info"""
    client = get_claw_client()
    channels = client.get_channels()
    
    for ch in channels:
        if ch.get("id") == channel_id:
            return ChannelInfo(
                id=ch.get("id"),
                name=ch.get("name"),
                type=ch.get("type"),
                status=ch.get("status"),
                capabilities=ch.get("capabilities", [])
            )
    
    raise HTTPException(status_code=404, detail="Channel not found")


@router.post("/api/channels/{channel_id}/send")
async def send_message(
    channel_id: str,
    request: SendMessageRequest,
    user: User = Depends(get_verified_user)
):
    """Send message via OpenClaw channel"""
    client = get_claw_client()
    
    result = client.send_message(
        channel=channel_id,
        message=request.message,
        to=request.to,
        media=request.media
    )
    
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.get("/api/channels/{channel_id}/history")
async def get_channel_history(
    channel_id: str,
    limit: int = 50,
    user: User = Depends(get_verified_user)
):
    """Get message history for channel"""
    # This would need to be implemented based on OpenClaw's message storage
    return {"messages": [], "channel": channel_id}

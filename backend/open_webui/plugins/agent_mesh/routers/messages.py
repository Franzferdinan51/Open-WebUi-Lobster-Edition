"""
Agent Mesh - Messages Router
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.models.users import User

from open_webui.plugins.agent_mesh import get_mesh_client, AgentMeshClient

log = logging.getLogger(__name__)
router = APIRouter()


class SendMessageRequest(BaseModel):
    from_agent_id: str
    to_agent_id: str
    message: str


@router.get("/api/mesh/messages")
async def list_messages(user: User = Depends(get_verified_user)):
    """List all messages"""
    client = get_mesh_client()
    messages = client.list_messages()
    return {"object": "list", "data": messages}


@router.post("/api/mesh/messages")
async def send_message(request: SendMessageRequest, user: User = Depends(get_verified_user)):
    """Send message to another agent"""
    client = get_mesh_client()
    result = client.send_message(
        from_agent_id=request.from_agent_id,
        to_agent_id=request.to_agent_id,
        message=request.message
    )
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/api/mesh/agents/{agent_id}/messages")
async def get_agent_messages(agent_id: str, user: User = Depends(get_verified_user)):
    """Get messages for specific agent"""
    client = get_mesh_client()
    messages = client.get_agent_messages(agent_id)
    return {"object": "list", "data": messages}


@router.get("/api/mesh/agents/{agent_id}/inbox")
async def get_agent_inbox(agent_id: str, user: User = Depends(get_verified_user)):
    """Get agent's inbox"""
    client = get_mesh_client()
    messages = client.get_agent_inbox(agent_id)
    return {"object": "list", "data": messages}


@router.delete("/api/mesh/messages/{message_id}")
async def delete_message(message_id: str, user: User = Depends(get_admin_user)):
    """Delete a message"""
    client = get_mesh_client()
    result = client.delete_message(message_id)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

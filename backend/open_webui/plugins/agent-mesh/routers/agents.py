"""
Agent Mesh - Agents Router
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.models.users import User

from open_webui.plugins.agent_mesh import get_mesh_client, AgentMeshClient

log = logging.getLogger(__name__)
router = APIRouter()


class RegisterAgentRequest(BaseModel):
    name: str
    endpoint: str
    capabilities: List[str]


class UpdateAgentRequest(BaseModel):
    name: Optional[str] = None
    endpoint: Optional[str] = None
    capabilities: Optional[List[str]] = None


@router.get("/api/mesh/agents")
async def list_agents(user: User = Depends(get_verified_user)):
    """List all registered agents"""
    client = get_mesh_client()
    agents = client.list_agents()
    return {"object": "list", "data": agents}


@router.post("/api/mesh/agents/register")
async def register_agent(request: RegisterAgentRequest, user: User = Depends(get_admin_user)):
    """Register or re-register an agent"""
    client = get_mesh_client()
    result = client.register_agent(
        name=request.name,
        endpoint=request.endpoint,
        capabilities=request.capabilities
    )
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/api/mesh/agents/{agent_id}")
async def get_agent(agent_id: str, user: User = Depends(get_verified_user)):
    """Get specific agent details"""
    client = get_mesh_client()
    agent = client.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/api/mesh/agents/{agent_id}")
async def update_agent(agent_id: str, request: UpdateAgentRequest, user: User = Depends(get_admin_user)):
    """Update agent information"""
    client = get_mesh_client()
    data = {k: v for k, v in request.dict().items() if v is not None}
    result = client.update_agent(agent_id, data)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.delete("/api/mesh/agents/{agent_id}")
async def delete_agent(agent_id: str, user: User = Depends(get_admin_user)):
    """Delete an agent"""
    client = get_mesh_client()
    result = client.delete_agent(agent_id)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

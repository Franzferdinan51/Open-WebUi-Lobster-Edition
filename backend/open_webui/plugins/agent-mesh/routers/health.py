"""
Agent Mesh - Health & Monitoring Router
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.models.users import User

from open_webui.plugins.agent_mesh import get_mesh_client, AgentMeshClient

log = logging.getLogger(__name__)
router = APIRouter()


class HealthMetrics(BaseModel):
    cpu: float
    memory: float
    disk: float
    uptime: float
    services: Dict[str, str]


@router.get("/api/mesh/health/dashboard")
async def health_dashboard(user: User = Depends(get_verified_user)):
    """Get health dashboard summary"""
    client = get_mesh_client()
    return client.get_health_dashboard()


@router.post("/api/mesh/agents/{agent_id}/health")
async def report_health(agent_id: str, metrics: HealthMetrics, user: User = Depends(get_verified_user)):
    """Report health metrics for agent"""
    client = get_mesh_client()
    result = client.report_health(agent_id, metrics.dict())
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/api/mesh/agents/{agent_id}/health")
async def get_agent_health(agent_id: str, user: User = Depends(get_verified_user)):
    """Get agent health details"""
    client = get_mesh_client()
    health = client.get_agent_health(agent_id)
    if not health:
        raise HTTPException(status_code=404, detail="Health data not found")
    return health


# ========== SYSTEM UPDATES ==========

class CreateUpdateRequest(BaseModel):
    version: str
    notes: str
    agent_id: str


@router.get("/api/mesh/updates")
async def list_updates(user: User = Depends(get_verified_user)):
    """List all system updates"""
    client = get_mesh_client()
    updates = client.list_updates()
    return {"object": "list", "data": updates}


@router.post("/api/mesh/updates")
async def create_update(request: CreateUpdateRequest, user: User = Depends(get_admin_user)):
    """Create system update"""
    client = get_mesh_client()
    result = client.create_update(
        version=request.version,
        notes=request.notes,
        agent_id=request.agent_id
    )
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/api/mesh/updates/{update_id}/acknowledge")
async def acknowledge_update(update_id: str, agent_id: str, user: User = Depends(get_verified_user)):
    """Acknowledge update"""
    client = get_mesh_client()
    result = client.acknowledge_update(update_id, agent_id)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# ========== CATASTROPHE PROTOCOLS ==========

class ReportCatastropheRequest(BaseModel):
    severity: str  # low, medium, high, critical
    description: str
    agent_id: str


@router.post("/api/mesh/catastrophe")
async def report_catastrophe(request: ReportCatastropheRequest, user: User = Depends(get_admin_user)):
    """Report catastrophe"""
    client = get_mesh_client()
    result = client.report_catastrophe(
        severity=request.severity,
        description=request.description,
        agent_id=request.agent_id
    )
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/atastrophe/protapi/mesh/cocols")
async def get_catastrophe_protocols(user: User = Depends(get_verified_user)):
    """Get recovery protocols"""
    client = get_mesh_client()
    return client.get_catastrophe_protocols()


# ========== STATUS ==========

@router.get("/api/mesh/status")
async def mesh_status(user: User = Depends(get_verified_user)):
    """Get Agent Mesh connection status"""
    client = get_mesh_client()
    return client.get_status()

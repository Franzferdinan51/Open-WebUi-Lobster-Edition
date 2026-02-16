"""
OpenClaw Control Panel - Agents, Cron, Sessions, Nodes, Logs
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.models.users import User

from open_webui.plugins.openclaw_control import get_control_client, OpenClawControlClient

log = logging.getLogger(__name__)
router = APIRouter()


# ========== AGENTS ==========

@router.get("/api/openclaw/agents")
async def list_agents(user: User = Depends(get_verified_user)):
    """List all OpenClaw agents"""
    client = get_control_client()
    agents = client.get_agents()
    return {"object": "list", "data": agents}


@router.get("/api/openclaw/agents/{agent_id}")
async def get_agent(agent_id: str, user: User = Depends(get_verified_user)):
    """Get specific agent"""
    client = get_control_client()
    agent = client.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


# ========== CRON JOBS ==========

@router.get("/api/openclaw/cron")
async def list_cron_jobs(user: User = Depends(get_verified_user)):
    """List all cron jobs"""
    client = get_control_client()
    jobs = client.get_cron_jobs()
    return {"object": "list", "data": jobs}


@router.post("/api/openclaw/cron")
async def create_cron_job(job: Dict[Any, Any], user: User = Depends(get_admin_user)):
    """Create cron job"""
    client = get_control_client()
    result = client.create_cron_job(job)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.delete("/api/openclaw/cron/{job_id}")
async def delete_cron_job(job_id: str, user: User = Depends(get_admin_user)):
    """Delete cron job"""
    client = get_control_client()
    result = client.delete_cron_job(job_id)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# ========== SESSIONS ==========

@router.get("/api/openclaw/sessions")
async def list_sessions(user: User = Depends(get_verified_user)):
    """List all sessions"""
    client = get_control_client()
    sessions = client.get_sessions()
    return {"object": "list", "data": sessions}


@router.get("/api/openclaw/sessions/{session_id}")
async def get_session(session_id: str, user: User = Depends(get_verified_user)):
    """Get specific session"""
    client = get_control_client()
    session = client.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


# ========== NODES ==========

@router.get("/api/openclaw/nodes")
async def list_nodes(user: User = Depends(get_verified_user)):
    """List all nodes"""
    client = get_control_client()
    nodes = client.get_nodes()
    return {"object": "list", "data": nodes}


# ========== LOGS ==========

@router.get("/api/openclaw/logs")
async def get_logs(limit: int = 100, user: User = Depends(get_admin_user)):
    """Get logs"""
    client = get_control_client()
    logs = client.get_logs(limit)
    return {"object": "list", "data": logs}

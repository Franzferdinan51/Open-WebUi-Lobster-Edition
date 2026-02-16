"""
OpenClaw Control Panel - Skills Router
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List

from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.models.users import User

from open_webui.plugins.openclaw_control import get_control_client, OpenClawControlClient

log = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/openclaw/skills")
async def list_skills(user: User = Depends(get_verified_user)):
    """List all OpenClaw skills"""
    client = get_control_client()
    skills = client.get_skills()
    return {"object": "list", "data": skills}


@router.post("/api/openclaw/skills/{skill_id}/enable")
async def enable_skill(skill_id: str, user: User = Depends(get_admin_user)):
    """Enable a skill"""
    client = get_control_client()
    result = client.enable_skill(skill_id)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/api/openclaw/skills/{skill_id}/disable")
async def disable_skill(skill_id: str, user: User = Depends(get_admin_user)):
    """Disable a skill"""
    client = get_control_client()
    result = client.disable_skill(skill_id)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

"""
OpenClaw Control Panel - Config Router
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.models.users import User

from open_webui.plugins.openclaw_control import get_control_client, OpenClawControlClient

log = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/openclaw/config")
async def get_config(user: User = Depends(get_verified_user)):
    """Get OpenClaw configuration"""
    client = get_control_client()
    return client.get_config()


@router.put("/api/openclaw/config")
async def update_config(config: Dict[Any, Any], user: User = Depends(get_admin_user)):
    """Update OpenClaw configuration"""
    client = get_control_client()
    result = client.update_config(config)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/api/openclaw/status")
async def get_status(user: User = Depends(get_verified_user)):
    """Get OpenClaw status"""
    client = get_control_client()
    return client.get_status()

"""
OpenClaw Auth Router - Use OpenClaw auth profiles
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


class AuthProfile(BaseModel):
    id: str
    provider: str
    mode: str  # oauth or api_key
    email: Optional[str] = None


@router.get("/api/auth/profiles")
async def list_auth_profiles(user: User = Depends(get_admin_user)):
    """List all OpenClaw auth profiles"""
    client = get_claw_client()
    profiles = client.get_auth_profiles()
    
    result = []
    for profile_id, profile_data in profiles.items():
        result.append(AuthProfile(
            id=profile_id,
            provider=profile_data.get("provider", "unknown"),
            mode=profile_data.get("mode", "api_key"),
            email=profile_data.get("email")
        ))
    
    return result


@router.get("/api/auth/status")
async def auth_status(user: User = Depends(get_verified_user)):
    """Get OpenClaw auth status"""
    client = get_claw_client()
    status = client.get_status()
    
    return {
        "connected": status.get("connected", False),
        "gateway_url": client.gateway_url,
        "profiles_count": len(client.get_auth_profiles())
    }


@router.post("/api/auth/sync")
async def sync_auth(user: User = Depends(get_admin_user)):
    """Sync auth from OpenClaw"""
    client = get_claw_client()
    profiles = client.get_auth_profiles()
    
    synced = []
    for profile_id, profile_data in profiles.items():
        synced.append({
            "id": profile_id,
            "provider": profile_data.get("provider"),
            "mode": profile_data.get("mode")
        })
    
    return {
        "synced": len(synced),
        "profiles": synced
    }

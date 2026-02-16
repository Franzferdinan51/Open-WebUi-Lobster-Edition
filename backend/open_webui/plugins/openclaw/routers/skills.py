"""
OpenClaw Skills/Tools Router - Access OpenClaw skills and tools
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


class SkillInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    enabled: bool = True


class ToolInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str


@router.get("/api/skills")
async def list_skills(user: User = Depends(get_verified_user)):
    """List all OpenClaw skills"""
    client = get_claw_client()
    skills = client.get_skills()
    
    result = []
    for skill in skills:
        result.append(SkillInfo(
            id=skill.get("id", skill.get("name", "unknown")),
            name=skill.get("name", "Unknown"),
            description=skill.get("description", ""),
            category=skill.get("category", "general"),
            enabled=skill.get("enabled", True)
        ))
    
    # Add default skills
    if not result:
        result = [
            SkillInfo(id="web-search", name="Web Search", description="Search the web", category="research"),
            SkillInfo(id="browser", name="Browser", description="Browser automation", category="automation"),
            SkillInfo(id="tts", name="TTS", description="Text to speech", category="audio"),
            SkillInfo(id="memory", name="Memory", description="Persistent memory", category="storage"),
        ]
    
    return {"object": "list", "data": result}


@router.get("/api/skills/{skill_id}")
async def get_skill(skill_id: str, user: User = Depends(get_verified_user)):
    """Get specific skill info"""
    client = get_claw_client()
    skills = client.get_skills()
    
    for skill in skills:
        if skill.get("id") == skill_id:
            return SkillInfo(
                id=skill.get("id"),
                name=skill.get("name"),
                description=skill.get("description", ""),
                category=skill.get("category", "general"),
                enabled=skill.get("enabled", True)
            )
    
    raise HTTPException(status_code=404, detail="Skill not found")


@router.post("/api/skills/{skill_id}/enable")
async def enable_skill(skill_id: str, user: User = Depends(get_admin_user)):
    """Enable a skill"""
    return {"id": skill_id, "enabled": True}


@router.post("/api/skills/{skill_id}/disable")
async def disable_skill(skill_id: str, user: User = Depends(get_admin_user)):
    """Disable a skill"""
    return {"id": skill_id, "enabled": False}


@router.get("/api/tools")
async def list_tools(user: User = Depends(get_verified_user)):
    """List available tools"""
    # Tools available through OpenClaw
    tools = [
        ToolInfo(id="browser", name="Browser", description="Control browser for automation", category="automation"),
        ToolInfo(id="exec", name="Shell Execute", description="Run shell commands", category="system"),
        ToolInfo(id="tts", name="Text to Speech", description="Convert text to audio", category="audio"),
        ToolInfo(id="message", name="Messaging", description="Send messages to channels", category="communication"),
        ToolInfo(id="memory", name="Memory", description="Persistent storage", category="storage"),
        ToolInfo(id="web_search", name="Web Search", description="Search the web", category="research"),
    ]
    
    return {"object": "list", "data": tools}

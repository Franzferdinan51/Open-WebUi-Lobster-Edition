"""
Generative UI - AG-UI Protocol Router

AG-UI (Agent-Generated UI) protocol for dynamic UI generation.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from open_webui.utils.auth import get_verified_user
from open_webui.models.users import User

from open_webui.plugins.generative_ui import get_generative_ui_service, GenerativeUIService

log = logging.getLogger(__name__)
router = APIRouter()


class Message(BaseModel):
    role: str  # user, assistant, system
    content: str


class Tool(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]


class AGUIRequest(BaseModel):
    messages: List[Message]
    tools: Optional[List[Tool]] = None
    stream: Optional[bool] = False


@router.post("/api/generative/agui/chat")
async def agui_chat(
    request: AGUIRequest,
    user: User = Depends(get_verified_user)
):
    """Chat with AG-UI protocol (Agent-Generated UI)"""
    service = get_generative_ui_service()
    
    messages = [m.dict() for m in request.messages]
    tools = [t.dict() if isinstance(t, Tool) else t for t in (request.tools or [])]
    
    response = service.generate_agui_response(messages, tools)
    
    return response


@router.get("/api/generative/agui/protocol")
async def get_protocol_info(user: User = Depends(get_verified_user)):
    """Get AG-UI protocol information"""
    return {
        "protocol": "ag-ui",
        "version": "1.0",
        "description": "Agent-Generated UI Protocol",
        "specification": "https://docs.copilotkit.ai/generative-ui",
        "features": [
            "dynamic_components",
            "tool_execution",
            "state_management",
            "human_in_the_loop"
        ]
    }


@router.get("/api/generative/agui/components")
async def get_agui_components(user: User = Depends(get_verified_user)):
    """Get AG-UI component specifications"""
    return {
        "components": [
            {
                "type": "text",
                "schema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string"},
                        "style": {"type": "object"}
                    }
                }
            },
            {
                "type": "button",
                "schema": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string"},
                        "action": {"type": "string"}
                    }
                }
            },
            {
                "type": "card",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "content": {"type": "string"},
                        "image": {"type": "string"},
                        "actions": {"type": "array"}
                    }
                }
            },
            {
                "type": "form",
                "schema": {
                    "type": "object",
                    "properties": {
                        "fields": {"type": "array"},
                        "submit_action": {"type": "string"}
                    }
                }
            },
            {
                "type": "chart",
                "schema": {
                    "type": "object",
                    "properties": {
                        "chart_type": {"type": "string"},
                        "data": {"type": "array"},
                        "labels": {"type": "array"}
                    }
                }
            },
        ]
    }

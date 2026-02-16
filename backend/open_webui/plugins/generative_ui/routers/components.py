"""
Generative UI - Components Router (CopilotKit-style)
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


class GenerateComponentRequest(BaseModel):
    type: str  # text, button, card, form, chart, table, list
    content: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    style: Optional[Dict[str, Any]] = None
    fields: Optional[List[Dict]] = None
    items: Optional[List[Dict]] = None
    columns: Optional[List[Dict]] = None
    rows: Optional[List[List]] = None
    chart_type: Optional[str] = "bar"
    labels: Optional[List[str]] = None
    title: Optional[str] = None
    image: Optional[str] = None
    actions: Optional[List[Dict]] = None
    label: Optional[str] = None
    action: Optional[str] = None


@router.post("/api/generative/ui/component")
async def generate_component(
    request: GenerateComponentRequest,
    user: User = Depends(get_verified_user)
):
    """Generate a UI component dynamically"""
    service = get_generative_ui_service()
    
    spec = request.dict(exclude_none=False)
    component = service.generate_ui_component(spec)
    
    return {
        "success": True,
        "component": component
    }


@router.post("/api/generative/ui/components")
async def generate_components(
    request: List[GenerateComponentRequest],
    user: User = Depends(get_verified_user)
):
    """Generate multiple UI components"""
    service = get_generative_ui_service()
    
    components = []
    for req in request:
        spec = req.dict(exclude_none=False)
        component = service.generate_ui_component(spec)
        components.append(component)
    
    return {
        "success": True,
        "components": components,
        "count": len(components)
    }


@router.get("/api/generative/ui/component/types")
async def get_component_types(user: User = Depends(get_verified_user)):
    """Get available component types"""
    return {
        "types": [
            {
                "id": "text",
                "name": "Text",
                "description": "Rich text content",
                "fields": ["content", "style"]
            },
            {
                "id": "button",
                "name": "Button",
                "description": "Interactive button",
                "fields": ["label", "action", "style"]
            },
            {
                "id": "card",
                "name": "Card",
                "description": "Content card with title and image",
                "fields": ["title", "content", "image", "actions"]
            },
            {
                "id": "form",
                "name": "Form",
                "description": "Input form",
                "fields": ["fields", "submit_action"]
            },
            {
                "id": "chart",
                "name": "Chart",
                "description": "Data visualization",
                "fields": ["chart_type", "data", "labels"]
            },
            {
                "id": "table",
                "name": "Table",
                "description": "Data table",
                "fields": ["columns", "rows"]
            },
            {
                "id": "list",
                "name": "List",
                "description": "List of items",
                "fields": ["items", "style"]
            },
        ]
    }

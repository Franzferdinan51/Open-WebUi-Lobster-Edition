"""
Generative UI - Search Router (Morphic-style AI Search)
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


class SearchRequest(BaseModel):
    query: str
    provider: Optional[str] = "brave"
    mode: Optional[str] = "adaptive"  # quick, planning, adaptive


class GenerateUIRequest(BaseModel):
    type: str  # text, button, card, form, chart, table, list
    content: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    style: Optional[Dict[str, Any]] = None


@router.get("/api/generative/search")
async def search(
    q: str,
    provider: str = "brave",
    mode: str = "adaptive",
    user: User = Depends(get_verified_user)
):
    """AI-powered search with generative results"""
    service = get_generative_ui_service()
    
    result = service.search(query=q, provider=provider)
    
    return {
        "query": q,
        "provider": provider,
        "mode": mode,
        "results": result.get("results", []),
        "generative_answer": result.get("generative_answer")
    }


@router.post("/api/generative/search")
async def search_post(
    request: SearchRequest,
    user: User = Depends(get_verified_user)
):
    """AI-powered search with generative results (POST)"""
    service = get_generative_ui_service()
    
    result = service.search(query=request.query, provider=request.provider)
    
    return {
        "query": request.query,
        "provider": request.provider,
        "mode": request.mode,
        "results": result.get("results", []),
        "generative_answer": result.get("generative_answer")
    }


@router.get("/api/generative/search/providers")
async def get_search_providers(user: User = Depends(get_verified_user)):
    """Get available search providers"""
    return {
        "providers": [
            {"id": "brave", "name": "Brave Search"},
            {"id": "searxng", "name": "SearXNG"},
            {"id": "exa", "name": "Exa"},
            {"id": "tavily", "name": "Tavily"},
        ],
        "modes": [
            {"id": "quick", "name": "Quick", "description": "Fast, concise results"},
            {"id": "planning", "name": "Planning", "description": "Detailed analysis"},
            {"id": "adaptive", "name": "Adaptive", "description": "AI-selected mode"},
        ]
    }


@router.get("/api/generative/search/modes")
async def get_search_modes(user: User = Depends(get_verified_user)):
    """Get available search modes"""
    return {
        "modes": [
            {"id": "quick", "name": "Quick", "description": "Fast, concise results"},
            {"id": "planning", "name": "Planning", "description": "Detailed analysis"},
            {"id": "adaptive", "name": "Adaptive", "description": "AI-selected mode"},
        ]
    }

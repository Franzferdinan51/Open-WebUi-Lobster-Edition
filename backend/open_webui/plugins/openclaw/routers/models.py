"""
OpenClaw Models Router - Expose OpenClaw models in OpenWebUI
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from open_webui.utils.auth import get_verified_user
from open_webui.models.users import User

from open_webui.plugins.openclaw import get_claw_client, OpenClawClient

log = logging.getLogger(__name__)
router = APIRouter()


class OpenAIModel(BaseModel):
    id: str
    object: str = "model"
    created: int = 1700000000
    owned_by: str = "openclaw"
    permission: List[Any] = []
    root: str = ""
    parent: Optional[str] = None


@router.get("/v1/models")
async def list_openclaw_models(user: User = Depends(get_verified_user)):
    """List all models from OpenClaw"""
    client = get_claw_client()
    claw_models = client.get_models()
    
    # Convert to OpenAI format
    models = []
    for m in claw_models:
        models.append(OpenAIModel(
            id=m.get("id", m.get("name", "unknown")),
            root=m.get("id", ""),
            owned_by=m.get("provider", "openclaw")
        ))
    
    # Add default models if no connection
    if not models:
        models = [
            OpenAIModel(id="openclaw:gpt-5.2", root="gpt-5.2", owned_by="openai"),
            OpenAIModel(id="openclaw:claude-opus", root="claude-opus", owned_by="anthropic"),
            OpenAIModel(id="openclaw:gemini-pro", root="gemini-pro", owned_by="google"),
        ]
    
    return {"object": "list", "data": models}


@router.get("/v1/models/{model_id}")
async def get_openclaw_model(model_id: str, user: User = Depends(get_verified_user)):
    """Get specific model info"""
    client = get_claw_client()
    claw_models = client.get_models()
    
    for m in claw_models:
        if m.get("id") == model_id or m.get("name") == model_id:
            return OpenAIModel(
                id=m.get("id", model_id),
                root=m.get("id", ""),
                owned_by=m.get("provider", "openclaw")
            )
    
    # Default response
    return OpenAIModel(
        id=model_id,
        root=model_id,
        owned_by="openclaw"
    )


@router.post("/v1/chat/completions")
async def chat_completions(
    request: Dict[Any, Any],
    user: User = Depends(get_verified_user)
):
    """Proxy chat completions through OpenClaw"""
    client = get_claw_client()
    
    model = request.get("model", "openclaw:gpt-5.2")
    messages = request.get("messages", [])
    stream = request.get("stream", False)
    
    # Remove openclaw: prefix for API call
    if model.startswith("openclaw:"):
        model = model[9:]
    
    # Build request
    kwargs = {
        "model": model,
        "messages": messages,
        "stream": stream
    }
    
    # Add optional params
    for param in ["temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty"]:
        if param in request:
            kwargs[param] = request[param]
    
    # Get response
    response = client.chat_completion(**kwargs)
    
    if stream:
        # Return streaming response
        return response
    else:
        # Return regular response
        if hasattr(response, 'json'):
            return response.json()
        return response

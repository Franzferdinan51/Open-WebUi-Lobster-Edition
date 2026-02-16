"""
OpenClaw Models Router - Expose OpenClaw models in OpenWebUI

Full compatibility with OpenAI API format.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from open_webui.utils.auth import get_verified_user
from open_webui.models.users import User

from open_webui.plugins.openclaw import get_claw_client, OpenClawClient
from open_webui.plugins.openclaw.compat import (
    is_openclaw_enabled,
    get_chat_completion_url,
    get_models_url,
    get_headers,
)

import requests
import json

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
async def list_openclaw_models():
    """List all models from OpenClaw (public endpoint)"""
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
    
    # Always add OpenClaw Agent
    models.append(OpenAIModel(
        id="openclaw-agent",
        root="openclaw-agent",
        owned_by="openclaw"
    ))
    
    # Add MiniMax models
    
    # Add LM Studio models (placeholder - actual models come from LM Studio server)
    models.append(OpenAIModel(id="lmstudio/qwen3-coder-next", root="qwen3-coder-next", owned_by="lmstudio"))
    models.append(OpenAIModel(id="lmstudio/qwen3-vl-30b-a3b-thinking", root="qwen3-vl-30b-a3b-thinking", owned_by="lmstudio"))
    models.append(OpenAIModel(id="lmstudio/jan-v3-4b-base-instruct", root="jan-v3-4b-base-instruct", owned_by="lmstudio"))
    models.append(OpenAIModel(id="lmstudio/lfm2.5-vl-1.6b", root="lfm2.5-vl-1.6b", owned_by="lmstudio"))
    
    return {"object": "list", "data": models}


@router.get("/v1/models/{model_id}")
async def get_openclaw_model(model_id: str):
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
    request: Request,
    user: User = Depends(get_verified_user)
):
    """Proxy chat completions through OpenClaw gateway"""
    
    # Check if OpenClaw is enabled
    if not is_openclaw_enabled():
        raise HTTPException(status_code=503, detail="OpenClaw integration is not enabled")
    
    # Get request body
    body = await request.json()
    
    model = body.get("model", "openclaw:gpt-5.2")
    messages = body.get("messages", [])
    stream = body.get("stream", False)
    
    # Remove openclaw: prefix if present
    if model.startswith("openclaw:"):
        model = model[9:]
    
    # Prepare request to OpenClaw
    url = get_chat_completion_url()
    headers = get_headers()
    headers["Content-Type"] = "application/json"
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream
    }
    
    # Add optional params
    for param in ["temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty", "stop"]:
        if param in body:
            payload[param] = body[param]
    
    try:
        if stream:
            # Handle streaming response
            response = requests.post(url, headers=headers, json=payload, stream=True, timeout=120)
            
            async def generate():
                for chunk in response.iter_content(chunk_size=None):
                    if chunk:
                        yield chunk
            
            return StreamingResponse(generate(), media_type="text/event-stream")
        else:
            # Handle regular response
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            
            if response.status_code != 200:
                log.error(f"OpenClaw API error: {response.status_code} - {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            return response.json()
    
    except Exception as e:
        log.error(f"Error calling OpenClaw: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/v1/embeddings")
async def embeddings(
    request: Request,
    user: User = Depends(get_verified_user)
):
    """Proxy embeddings through OpenClaw"""
    
    if not is_openclaw_enabled():
        raise HTTPException(status_code=503, detail="OpenClaw integration is not enabled")
    
    body = await request.json()
    model = body.get("model", "text-embedding-ada-002")
    input_text = body.get("input", "")
    
    from open_webui.plugins.openclaw.compat import get_embeddings_url
    
    url = get_embeddings_url()
    headers = get_headers()
    headers["Content-Type"] = "application/json"
    
    payload = {
        "model": model,
        "input": input_text
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        return response.json()
    except Exception as e:
        log.error(f"Error calling OpenClaw embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

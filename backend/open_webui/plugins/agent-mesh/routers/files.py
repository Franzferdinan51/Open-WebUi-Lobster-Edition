"""
Agent Mesh - Files Router
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List

from open_webui.utils.auth import get_verified_user, get_admin_user
from open_webui.models.users import User

from open_webui.plugins.agent_mesh import get_mesh_client, AgentMeshClient

log = logging.getLogger(__name__)
router = APIRouter()


class UploadFileRequest(BaseModel):
    filename: str
    content: str  # Base64 encoded
    agent_id: str


@router.get("/api/mesh/files")
async def list_files(user: User = Depends(get_verified_user)):
    """List all files in mesh"""
    client = get_mesh_client()
    files = client.list_files()
    return {"object": "list", "data": files}


@router.post("/api/mesh/files")
async def upload_file(request: UploadFileRequest, user: User = Depends(get_verified_user)):
    """Upload file to mesh (Base64)"""
    client = get_mesh_client()
    result = client.upload_file(
        filename=request.filename,
        content=request.content,
        agent_id=request.agent_id
    )
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/api/mesh/files/{file_id}")
async def get_file(file_id: str, user: User = Depends(get_verified_user)):
    """Download file"""
    client = get_mesh_client()
    file_data = client.get_file(file_id)
    if not file_data or file_data.get("error"):
        raise HTTPException(status_code=404, detail="File not found")
    return file_data


@router.delete("/api/mesh/files/{file_id}")
async def delete_file(file_id: str, user: User = Depends(get_admin_user)):
    """Delete a file"""
    client = get_mesh_client()
    result = client.delete_file(file_id) if hasattr(client, 'delete_file') else {"error": "Not implemented"}
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

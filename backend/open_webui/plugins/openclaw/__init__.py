"""
OpenClaw Integration Plugin for OpenWebUI

Full OpenClaw compatibility - models, auth, channels, tools.
"""

import os
import logging
from typing import Optional

from fastapi import APIRouter

log = logging.getLogger(__name__)

# OpenClaw Configuration - from env.py
from open_webui.env import OPENCLAW_GATEWAY_URL, OPENCLAW_GATEWAY_KEY, OPENCLAW_ENABLED


class OpenClawClient:
    """Client for OpenClaw Gateway API"""
    
    def __init__(self, gateway_url: str = None, api_key: str = None):
        self.gateway_url = gateway_url or OPENCLAW_GATEWAY_URL
        self.api_key = api_key or OPENCLAW_GATEWAY_KEY
        self._connected = False
        
    def _make_request(self, method: str, endpoint: str, **kwargs):
        """Make HTTP request to gateway"""
        import requests
        url = f"{self.gateway_url}{endpoint}"
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            response = requests.request(method, url, headers=headers, timeout=5, **kwargs)
            if response.status_code == 200:
                self._connected = True
                return response.json()
        except Exception:
            self._connected = False
        return None
    
    def get_models(self):
        """Get all configured models from OpenClaw"""
        result = self._make_request("GET", "/api/models")
        if result:
            return result.get("data", [])
        return []
    
    def get_auth_profiles(self):
        """Get auth profiles from OpenClaw"""
        result = self._make_request("GET", "/api/auth/profiles")
        if result:
            return result
        return {}
    
    def get_channels(self):
        """Get configured channels from OpenClaw"""
        result = self._make_request("GET", "/api/channels")
        if result:
            return result.get("data", [])
        return []
    
    def get_skills(self):
        """Get installed skills from OpenClaw"""
        result = self._make_request("GET", "/api/skills")
        if result:
            return result.get("data", [])
        return []
    
    def send_message(self, channel: str, message: str, **kwargs):
        """Send message via OpenClaw channel"""
        return self._make_request("POST", f"/api/channels/{channel}/send", json={"message": message, **kwargs})
    
    def chat_completion(self, model: str, messages: list, **kwargs):
        """Send chat completion request through OpenClaw"""
        return self._make_request("POST", "/v1/chat/completions", json={
            "model": model,
            "messages": messages,
            **kwargs
        })
    
    def get_status(self):
        """Get OpenClaw gateway status"""
        result = self._make_request("GET", "/api/status")
        return {"connected": self._connected, "status": result}


# Global client instance
_claw_client: Optional[OpenClawClient] = None


def get_claw_client() -> OpenClawClient:
    """Get or create OpenClaw client"""
    global _claw_client
    if _claw_client is None:
        _claw_client = OpenClawClient()
    return _claw_client


def init_openclaw_plugin():
    """Initialize the OpenClaw plugin - called on startup"""
    log.info("Initializing OpenClaw Plugin for OpenWebUI")
    
    # Import and include routers
    from open_webui.plugins.openclaw.routers import models, auth, channels, skills
    
    # Return plugin info
    return {
        "name": "OpenClaw Integration",
        "version": "1.0.0",
        "description": "Full OpenClaw compatibility for OpenWebUI",
        "routers": ["models", "auth", "channels", "skills"]
    }

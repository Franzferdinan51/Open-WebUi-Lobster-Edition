"""
OpenClaw Control Panel Plugin for OpenWebUI

Provides access to OpenClaw settings, channels, skills, agents, cron jobs, 
sessions, nodes, and more - allowing users to control their OpenClaw 
instance from OpenWebUI Lobster Edition.
"""

import os
import logging
from typing import Optional, Dict, Any, List

import requests
from pydantic import BaseModel

log = logging.getLogger(__name__)

# Configuration
OPENCLAW_GATEWAY_URL = os.environ.get("OPENCLAW_GATEWAY_URL", "http://localhost:18789")
OPENCLAW_GATEWAY_KEY = os.environ.get("OPENCLAW_GATEWAY_KEY", "")


class OpenClawControlClient:
    """Client for controlling OpenClaw via its API"""
    
    def __init__(self, gateway_url: str = None, api_key: str = None):
        self.gateway_url = gateway_url or OPENCLAW_GATEWAY_URL
        self.api_key = api_key or OPENCLAW_GATEWAY_KEY
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    # ========== CONFIG ==========
    
    def get_config(self) -> Dict[str, Any]:
        """Get OpenClaw configuration"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/config")
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            log.error(f"Failed to get config: {e}")
            return {}
    
    def update_config(self, config: Dict) -> Dict:
        """Update OpenClaw configuration"""
        try:
            response = self.session.put(f"{self.gateway_url}/api/config", json=config)
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    # ========== CHANNELS ==========
    
    def get_channels(self) -> List[Dict]:
        """Get all channels"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/channels")
            return response.json().get("data", []) if response.status_code == 200 else []
        except Exception:
            return []
    
    def get_channel(self, channel_id: str) -> Dict:
        """Get specific channel"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/channels/{channel_id}")
            return response.json() if response.status_code == 200 else {}
        except Exception:
            return {}
    
    def update_channel(self, channel_id: str, config: Dict) -> Dict:
        """Update channel configuration"""
        try:
            response = self.session.put(f"{self.gateway_url}/api/channels/{channel_id}", json=config)
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    # ========== SKILLS ==========
    
    def get_skills(self) -> List[Dict]:
        """Get all skills"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/skills")
            return response.json().get("data", []) if response.status_code == 200 else []
        except Exception:
            return []
    
    def enable_skill(self, skill_id: str) -> Dict:
        """Enable a skill"""
        try:
            response = self.session.post(f"{self.gateway_url}/api/skills/{skill_id}/enable")
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def disable_skill(self, skill_id: str) -> Dict:
        """Disable a skill"""
        try:
            response = self.session.post(f"{self.gateway_url}/api/skills/{skill_id}/disable")
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    # ========== AGENTS ==========
    
    def get_agents(self) -> List[Dict]:
        """Get all agents"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/agents")
            return response.json().get("data", []) if response.status_code == 200 else []
        except Exception:
            return []
    
    def get_agent(self, agent_id: str) -> Dict:
        """Get specific agent"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/agents/{agent_id}")
            return response.json() if response.status_code == 200 else {}
        except Exception:
            return {}
    
    # ========== CRON JOBS ==========
    
    def get_cron_jobs(self) -> List[Dict]:
        """Get all cron jobs"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/cron")
            return response.json().get("data", []) if response.status_code == 200 else []
        except Exception:
            return []
    
    def create_cron_job(self, job: Dict) -> Dict:
        """Create cron job"""
        try:
            response = self.session.post(f"{self.gateway_url}/api/cron", json=job)
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def delete_cron_job(self, job_id: str) -> Dict:
        """Delete cron job"""
        try:
            response = self.session.delete(f"{self.gateway_url}/api/cron/{job_id}")
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    # ========== SESSIONS ==========
    
    def get_sessions(self) -> List[Dict]:
        """Get all sessions"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/sessions")
            return response.json().get("data", []) if response.status_code == 200 else []
        except Exception:
            return []
    
    def get_session(self, session_id: str) -> Dict:
        """Get specific session"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/sessions/{session_id}")
            return response.json() if response.status_code == 200 else {}
        except Exception:
            return {}
    
    # ========== NODES ==========
    
    def get_nodes(self) -> List[Dict]:
        """Get all nodes"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/nodes")
            return response.json().get("data", []) if response.status_code == 200 else []
        except Exception:
            return []
    
    # ========== LOGS ==========
    
    def get_logs(self, limit: int = 100) -> List[Dict]:
        """Get logs"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/logs?limit={limit}")
            return response.json().get("data", []) if response.status_code == 200 else []
        except Exception:
            return []
    
    # ========== STATUS ==========
    
    def get_status(self) -> Dict:
        """Get OpenClaw status"""
        try:
            response = self.session.get(f"{self.gateway_url}/api/status")
            return response.json() if response.status_code == 200 else {"connected": False}
        except Exception:
            return {"connected": False, "error": "Cannot connect"}


# Global client
_control_client: Optional[OpenClawControlClient] = None


def get_control_client() -> OpenClawControlClient:
    """Get or create control client"""
    global _control_client
    if _control_client is None:
        _control_client = OpenClawControlClient()
    return _control_client


def init_openclaw_control_plugin():
    """Initialize the control panel plugin"""
    log.info("Initializing OpenClaw Control Panel for OpenWebUI")
    client = get_control_client()
    status = client.get_status()
    log.info(f"OpenClaw Control: {status}")
    return status

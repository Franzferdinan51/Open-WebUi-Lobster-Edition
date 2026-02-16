"""
Agent Mesh Plugin for OpenWebUI

Full Agent Mesh API integration - multi-agent communication, file sharing, health monitoring.
"""

import os
import logging
from typing import Optional, Dict, Any, List

import requests
from pydantic import BaseModel

log = logging.getLogger(__name__)

# Agent Mesh Configuration
AGENT_MESH_URL = os.environ.get("AGENT_MESH_URL", "http://localhost:4000")
AGENT_MESH_KEY = os.environ.get("AGENT_MESH_KEY", "openclaw-mesh-default-key")


class AgentMeshClient:
    """Client for Agent Mesh API"""
    
    def __init__(self, mesh_url: str = None, api_key: str = None):
        self.mesh_url = mesh_url or AGENT_MESH_URL
        self.api_key = api_key or AGENT_MESH_KEY
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        })
    
    # ========== AGENT MANAGEMENT ==========
    
    def register_agent(self, name: str, endpoint: str, capabilities: List[str]) -> Dict:
        """Register or re-register an agent"""
        try:
            response = self.session.post(
                f"{self.mesh_url}/api/agents/register",
                json={"name": name, "endpoint": endpoint, "capabilities": capabilities}
            )
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def list_agents(self) -> List[Dict]:
        """List all registered agents"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/agents")
            return response.json() if response.status_code == 200 else []
        except Exception:
            return []
    
    def get_agent(self, agent_id: str) -> Dict:
        """Get specific agent details"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/agents/{agent_id}")
            return response.json() if response.status_code == 200 else {}
        except Exception:
            return {}
    
    def update_agent(self, agent_id: str, data: Dict) -> Dict:
        """Update agent information"""
        try:
            response = self.session.put(f"{self.mesh_url}/api/agents/{agent_id}", json=data)
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def delete_agent(self, agent_id: str) -> Dict:
        """Delete an agent"""
        try:
            response = self.session.delete(f"{self.mesh_url}/api/agents/{agent_id}")
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    # ========== MESSAGING ==========
    
    def send_message(self, from_agent_id: str, to_agent_id: str, message: str) -> Dict:
        """Send message to another agent"""
        try:
            response = self.session.post(
                f"{self.mesh_url}/api/messages",
                json={
                    "fromAgentId": from_agent_id,
                    "toAgentId": to_agent_id,
                    "message": message
                }
            )
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def list_messages(self) -> List[Dict]:
        """List all messages"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/messages")
            return response.json() if response.status_code == 200 else []
        except Exception:
            return []
    
    def get_agent_messages(self, agent_id: str) -> List[Dict]:
        """Get messages for specific agent"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/agents/{agent_id}/messages")
            return response.json() if response.status_code == 200 else []
        except Exception:
            return []
    
    def get_agent_inbox(self, agent_id: str) -> List[Dict]:
        """Get agent's inbox"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/agents/{agent_id}/inbox")
            return response.json() if response.status_code == 200 else []
        except Exception:
            return []
    
    def delete_message(self, message_id: str) -> Dict:
        """Delete a message"""
        try:
            response = self.session.delete(f"{self.mesh_url}/api/messages/{message_id}")
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    # ========== FILE TRANSFER ==========
    
    def upload_file(self, filename: str, content: str, agent_id: str) -> Dict:
        """Upload file to mesh (Base64)"""
        try:
            response = self.session.post(
                f"{self.mesh_url}/api/files/upload",
                json={"filename": filename, "content": content, "agentId": agent_id}
            )
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def get_file(self, file_id: str) -> Dict:
        """Download file"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/files/{file_id}")
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception:
            return {}
    
    def list_files(self) -> List[Dict]:
        """List all files"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/files")
            return response.json() if response.status_code == 200 else []
        except Exception:
            return []
    
    # ========== HEALTH MONITORING ==========
    
    def report_health(self, agent_id: str, metrics: Dict) -> Dict:
        """Report health metrics"""
        try:
            response = self.session.post(
                f"{self.mesh_url}/api/agents/{agent_id}/health",
                json=metrics
            )
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def get_agent_health(self, agent_id: str) -> Dict:
        """Get agent health details"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/agents/{agent_id}/health")
            return response.json() if response.status_code == 200 else {}
        except Exception:
            return {}
    
    def get_health_dashboard(self) -> Dict:
        """Get health dashboard summary"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/health/dashboard")
            return response.json() if response.status_code == 200 else {}
        except Exception:
            return {}
    
    # ========== SYSTEM UPDATES ==========
    
    def create_update(self, version: str, notes: str, agent_id: str) -> Dict:
        """Create system update"""
        try:
            response = self.session.post(
                f"{self.mesh_url}/api/updates",
                json={"version": version, "notes": notes, "agentId": agent_id}
            )
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def list_updates(self) -> List[Dict]:
        """List all updates"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/updates")
            return response.json() if response.status_code == 200 else []
        except Exception:
            return []
    
    def acknowledge_update(self, update_id: str, agent_id: str) -> Dict:
        """Acknowledge update"""
        try:
            response = self.session.post(
                f"{self.mesh_url}/api/updates/{update_id}/acknowledge",
                json={"agentId": agent_id}
            )
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    # ========== CATASTROPHE PROTOCOLS ==========
    
    def report_catastrophe(self, severity: str, description: str, agent_id: str) -> Dict:
        """Report catastrophe"""
        try:
            response = self.session.post(
                f"{self.mesh_url}/api/catastrophe",
                json={"severity": severity, "description": description, "agentId": agent_id}
            )
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def get_catastrophe_protocols(self) -> Dict:
        """Get recovery protocols"""
        try:
            response = self.session.get(f"{self.mesh_url}/api/catastrophe/protocols")
            return response.json() if response.status_code == 200 else {}
        except Exception:
            return {}
    
    # ========== STATUS ==========
    
    def get_status(self) -> Dict:
        """Get Agent Mesh connection status"""
        try:
            agents = self.list_agents()
            return {
                "connected": True,
                "agents_count": len(agents),
                "mesh_url": self.mesh_url
            }
        except Exception:
            return {"connected": False, "error": "Cannot connect to Agent Mesh"}


# Global client instance
_mesh_client: Optional[AgentMeshClient] = None


def get_mesh_client() -> AgentMeshClient:
    """Get or create Agent Mesh client"""
    global _mesh_client
    if _mesh_client is None:
        _mesh_client = AgentMeshClient()
    return _mesh_client


def init_agent_mesh_plugin():
    """Initialize the Agent Mesh plugin"""
    log.info("Initializing Agent Mesh Plugin for OpenWebUI")
    client = get_mesh_client()
    status = client.get_status()
    log.info(f"Agent Mesh Status: {status}")
    return status

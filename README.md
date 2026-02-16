# OpenWebUI Lobster Edition - OpenClaw Compatible

<p align="center">
  <img src="banner.png" alt="OpenWebUI Lobster Edition" width="500">
</p>

<p align="center">
  <strong>OpenWebUI with Full OpenClaw Integration</strong>
</p>

This is **OpenWebUI Lobster Edition** - a fork of OpenWebUI with **full OpenClaw integration** built-in.

## 🌟 Features

### OpenClaw Integration (Full)

- 🔐 **OpenClaw Authentication** - Use OpenClaw auth profiles (OAuth + API keys)
- 🤖 **OpenClaw Models** - Access all OpenClaw configured models seamlessly
- 💬 **OpenClaw Channels** - Telegram, WhatsApp, Discord, Slack, Signal, iMessage
- 🛠️ **OpenClaw Tools** - Browser, TTS, Canvas, Memory, Agents
- 📡 **Gateway Proxy** - Route requests through OpenClaw gateway
- 🔄 **Bidirectional Sync** - Keep models/channels in sync
- 🌐 **OpenAI Compatible** - All /v1/* endpoints work with OpenClaw

### Agent Mesh Integration (Full)

- 🤝 **Multi-Agent Communication** - Agent-to-agent messaging
- 📋 **Agent Registry** - Register and discover agents
- ❤️ **Health Monitoring** - Real-time agent health dashboard
- 📁 **File Transfer** - Share files between agents
- 🔄 **System Updates** - Centralized update management
- 🛡️ **Catastrophe Protocols** - Recovery procedures
- 📊 **Mesh Dashboard** - View all agents and status

### Original OpenWebUI Features (All Included)

- 🚀 **Intuitive UI** - For Ollama, OpenAI, LM Studio, and compatible APIs
- 📱 **Mobile-Responsive** - Full support for mobile and tablet
- 🔌 **Plugin System** - Extensible with custom functions and tools
- 💾 **Chat History** - Persistent conversations with search
- 📤 **File Upload** - PDF, images, documents with OCR
- 🧠 **RAG** - Retrieval-Augmented Generation with knowledge bases
- 🎨 **Themes** - Customizable dark/light modes
- 🌐 **i18n** - Multi-language support (50+ languages)
- 📊 **Analytics** - Usage tracking and insights
- 🔧 **Function Calling** - Built-in tools and external integrations
- 📚 **Knowledge Bases** - Create and manage document collections
- 👥 **Multi-User** - Team collaboration with roles
- 🔐 **Admin Panel** - Full user and system management
- 📖 **Prompt Library** - Save and share prompts
- 🎯 **Models** - Support for 100+ AI models
- 🗣️ **Voice** - Text-to-speech and voice input
- 🖼️ **Image Generation** - Built-in image generation support
- 📝 **Code Highlighting** - Syntax highlighting for 100+ languages

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/Franzferdinan51/open-webui-Lobster-compatable.git
cd open-webui-Lobster-compatable

# Start with Docker
docker-compose up -d

# Or run locally
cd backend
pip install -r requirements.txt
./start.sh
```

### Environment Variables

```bash
# OpenClaw Gateway Configuration
OPENCLAW_GATEWAY_URL=http://localhost:18789
OPENCLAW_GATEWAY_KEY=your-api-key
OPENCLAW_ENABLED=true

# Agent Mesh Configuration
AGENT_MESH_URL=http://localhost:4000
AGENT_MESH_KEY=openclaw-mesh-default-key
AGENT_MESH_ENABLED=true
```

## 📡 OpenClaw API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/openclaw/v1/models` | List OpenClaw models |
| `/openclaw/v1/chat/completions` | Chat completions (OpenAI compatible) |
| `/openclaw/v1/embeddings` | Embeddings (OpenAI compatible) |
| `/openclaw/api/auth/profiles` | Auth profiles |
| `/openclaw/api/channels` | List channels |
| `/openclaw/api/channels/{id}/send` | Send message |
| `/openclaw/api/skills` | List skills |
| `/openclaw/api/sync` | Sync models from OpenClaw |
| `/openclaw/api/status` | Get OpenClaw connection status |

## 📡 Agent Mesh API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/agent-mesh/api/mesh/agents` | List all agents |
| `/agent-mesh/api/mesh/agents/register` | Register agent |
| `/agent-mesh/api/mesh/messages` | Send message between agents |
| `/agent-mesh/api/mesh/health/dashboard` | Health dashboard |
| `/agent-mesh/api/mesh/files` | File transfer |
| `/agent-mesh/api/mesh/updates` | System updates |
| `/agent-mesh/api/mesh/catastrophe` | Catastrophe reporting |
| `/agent-mesh/api/mesh/status` | Mesh connection status |

## 🔌 Compatibility

### OpenAI API Compatibility
All `/v1/*` endpoints are compatible with OpenAI API:
- `/v1/models` - List models
- `/v1/chat/completions` - Chat completions
- `/v1/embeddings` - Text embeddings
- `/v1/images` - Image generation (via OpenClaw)

### Ollama Compatibility
Ollama requests can be routed through OpenClaw:
```bash
OLLAMA_BASE_URL=http://localhost:18789/v1
```

### LM Studio Compatibility
LM Studio works with OpenClaw models:
```bash
OPENAI_BASE_URL=http://localhost:18789/v1
```

## 🛠️ Configuration

### OpenClaw Gateway

Connect to remote gateway via Tailscale:
```bash
OPENCLAW_GATEWAY_URL=http://100.106.80.61:18789
```

### Models Supported

- Ollama models (100+)
- OpenAI models (GPT-4, GPT-3.5, DALL-E)
- LM Studio models
- Anthropic (via OpenAI-compatible API)
- Google Gemini (via OpenAI-compatible API)
- xAI Grok
- Cohere
- Mistral
- And all OpenClaw-configured models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - Based on OpenWebUI

## 💰 Support Development

If you find OpenWebUI Lobster Edition useful:

**Bitcoin:** `bc1q733czwuelntfug8jgur6md2lhzcx7l5ufks9y7`

---

**Repository:** https://github.com/Franzferdinan51/open-webui-Lobster-compatable  
**Original OpenWebUI:** https://github.com/open-webui/open-webui  
**OpenClaw:** https://github.com/openclaw/openclaw

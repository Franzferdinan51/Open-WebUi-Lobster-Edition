# OpenWebUI Lobster Edition - OpenClaw Agent First WebUI

<p align="center">
  <img src="banner.png" alt="OpenWebUI Lobster Edition" width="500">
</p>

<p align="center">
  <strong>🦞 OpenClaw Agent First WebUI - Built for Multi-Agent AI Orchestration</strong>
</p>

This is **OpenWebUI Lobster Edition** - the **first WebUI designed specifically for OpenClaw agents** with full OpenClaw integration built-in.

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

### OpenClaw Control Panel

- ⚙️ **Config Management** - View/edit OpenClaw configuration
- 📱 **Channel Control** - Manage Telegram, WhatsApp, Discord, Slack, Signal, iMessage
- 🛠️ **Skills Control** - Enable/disable OpenClaw skills
- 🤖 **Agent Management** - View and manage agents
- ⏰ **Cron Jobs** - Create and manage scheduled tasks
- 💻 **Session Management** - View active sessions
- 🌐 **Node Management** - View connected nodes
- 📋 **Logs** - View OpenClaw logs

### Generative UI (NEW)

- 🔮 **AI Search** - Morphic-style generative search (Brave, SearXNG, Exa, Tavily)
- 🎨 **Dynamic Components** - CopilotKit-style generative UI components
- 📡 **AG-UI Protocol** - Agent-Generated UI protocol support
- 🃏 **UI Cards** - AI-generated content cards
- 📊 **Charts** - Dynamic chart generation
- 📝 **Forms** - AI-generated input forms
- 📋 **Tables** - Dynamic data tables

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

## 🛠️ Menus & Settings

### Custom Admin Menus

- **OpenClaw** - Gateway status, model sync, channel management
- **Agent Mesh** - Agent registry, health, file sharing
- **Control Panel** - Full OpenClaw admin controls

### Settings Pages

| Page | Features |
|------|----------|
| **General** | OpenClaw gateway URL, API key, sync settings |
| **Models** | OpenClaw model sync, LM Studio, Ollama, MiniMax |
| **Connections** | Agent Mesh, ComfyUI, external APIs |
| **Channels** | Telegram, WhatsApp, Discord, Slack management |
| **Tools** | Browser, TTS, Canvas, custom tools |
| **Audio** | TTS/STT configuration |
| **Images** | Image generation settings |
| **Web Search** | Brave, SearXNG, Tavily configuration |
| **Code Execution** | Python, JavaScript runtime |

### Default Configuration

The Lobster Edition comes pre-configured to connect to your OpenClaw instance:

```bash
# Default model sources (in priority order)
DEFAULT_MODELS="openclaw/*,lmstudio/*,minimax-portal/*"
DEFAULT_PINNED_MODELS="openclaw/gpt-5.2,lmstudio/qwen3-coder-next,minimax-portal/MiniMax-M2.5"

# OpenClaw Gateway as primary
OLLAMA_API_BASE_URL="http://localhost:18789/v1"
OPENAI_API_BASE_URL="http://localhost:18789/v1"
```

### DuckBot Features (Enabled by Default)

- 🤖 **Agent Smith** - Connected via Agent Mesh
- 🧠 **MiniMax M2.5** - Primary reasoning model
- 💻 **LM Studio** - Local coding models (Qwen3, etc.)
- 🎨 **ComfyUI** - Distributed image generation
- 🔊 **TTS** - Real-time voice synthesis
- 🌐 **Multi-Agent** - Distributed AI orchestration

## 🦞 DuckBot Settings Tab

The Lobster Edition includes a dedicated **DuckBot Settings** page in the admin panel with:

### Quick Links
- 📊 Dashboard - `http://localhost:5000`
- 🔧 ClawAPI - `http://localhost:5001`
- 🎨 ComfyUI - `http://localhost:8188`
- 📚 API Docs - `http://localhost:18789/docs`

### Model Presets
- 🔌 **OpenClaw Gateway (WebSocket)** - `ws://localhost:18789` - Control Plane
- 🤖 **OpenClaw Gateway (HTTP)** - `http://localhost:18789/v1` - Model API
- 🤖 **MiniMax Portal** - Cloud models
- 🦙 **LM Studio** - Local models
- 🦙 **Ollama** - Local models

### Agent Connections
- 🤖 Agent Smith status
- 🌐 Agent Mesh URL
- 🔗 OpenClaw Gateway
- 🎨 ComfyUI

### Tools & Features
- 🔊 Text-to-Speech (KaniTTS)
- ₿ Crypto Tracking
- 📈 Polymarket Integration
- 📱 Social Media (disabled)

### 🎨 Lobster Theme
Select **🦞 Lobster** from the theme dropdown in Settings → General to activate the custom orange/red lobster-themed UI.

## 📡 OpenClaw Control Panel Endpoints

| Endpoint | Description |
|----------|-------------|
| `/openclaw-control/api/openclaw/config` | Get/update config |
| `/openclaw-control/api/openclaw/status` | Gateway status |
| `/openclaw-control/api/openclaw/channels` | Manage channels |
| `/openclaw-control/api/openclaw/skills` | Manage skills |
| `/openclaw-control/api/openclaw/agents` | View agents |
| `/openclaw-control/api/openclaw/cron` | Manage cron jobs |
| `/openclaw-control/api/openclaw/sessions` | View sessions |
| `/openclaw-control/api/openclaw/nodes` | View nodes |
| `/openclaw-control/api/openclaw/logs` | View logs |

## 📡 Generative UI Endpoints

| Endpoint | Description |
|----------|-------------|
| `/generative-ui/api/generative/search` | AI-powered search |
| `/generative-ui/api/generative/search/providers` | Search providers |
| `/generative-ui/api/generative/ui/component` | Generate UI component |
| `/generative-ui/api/generative/ui/component/types` | Component types |
| `/generative-ui/api/generative/agui/chat` | AG-UI chat |
| `/generative-ui/api/generative/agui/protocol` | Protocol info |

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
OPENCLAW_GATEWAY_URL=http://localhost:18789
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

## 🦞 Credits

**OpenClaw Agent First WebUI** - Built for Multi-Agent AI Orchestration

### Built With
- 🦞 **DuckBot** - The AI assistant running this instance
- 🤖 **Agent Smith** - Windows agent partner
- 🌐 **Agent Mesh** - Multi-agent communication network
- 🔗 **OpenClaw** - The agent framework powering it all

### Generative UI Inspired By
- 🎨 **Morphic** - AI-generated interfaces
- 🃏 **CopilotKit** - Copilot-style UI components
- 📡 **AG-UI Protocol** - Agent-Generated UI protocol
- 🔍 **Brave Search** - Web search integration
- 🧠 **Exa/Tavily** - AI-powered search

### Links

**Repository:** https://github.com/Franzferdinan51/Open-WebUi-Lobster-Edition  
**OpenClaw:** https://github.com/openclaw/openclaw  
**OpenWebUI:** https://github.com/open-webui/open-webui  
**Agent Mesh:** https://github.com/Franzferdinan51/agent-mesh-api  
**ClawHub:** https://clawhub.com

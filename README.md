# OpenWebUI Lobster Edition - OpenClaw Compatible

<p align="center">
  <img src="../../banner.png" alt="OpenWebUI Lobster Edition" width="500">
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

### Original OpenWebUI Features

- 🚀 Intuitive UI for Ollama, OpenAI, and compatible APIs
- 📱 Mobile-responsive design
- 🔌 Extensible plugin system
- 💾 Persistent chat history
- 📤 File upload support
- 🧠 RAG (Retrieval-Augmented Generation)
- 🎨 Customizable themes
- 🌐 Multi-language support
- 📊 Usage analytics
- 🔧 Function calling
- 📚 Knowledge base management

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
```

## 📡 OpenClaw API Endpoints

Once running, access OpenClaw through these endpoints:

| Endpoint | Description |
|----------|-------------|
| `/openclaw/v1/models` | List OpenClaw models |
| `/openclaw/v1/chat/completions` | Chat completions |
| `/openclaw/api/auth/profiles` | Auth profiles |
| `/openclaw/api/channels` | List channels |
| `/openclaw/api/channels/{id}/send` | Send message |
| `/openclaw/api/skills` | List skills |

## 🛠️ Configuration

### OpenClaw Gateway

By default, connects to `http://localhost:18789`. To connect to a remote gateway:

```bash
# Connect to remote OpenClaw (e.g., via Tailscale)
OPENCLAW_GATEWAY_URL=http://100.106.80.61:18789
```

### Models

All OpenClaw models automatically appear in the model selector.

### Channels

Configure channels in OpenClaw - they sync automatically.

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

# OpenClaw Plugin for OpenWebUI

This plugin provides full OpenClaw integration for OpenWebUI Lobster Edition.

## Features

- 🔐 **OpenClaw Authentication** - Use OpenClaw auth profiles (OAuth + API keys)
- 🤖 **OpenClaw Models** - Access all OpenClaw configured models
- 💬 **OpenClaw Channels** - Telegram, WhatsApp, Discord, Slack, Signal, iMessage
- 🛠️ **OpenClaw Tools** - Browser, TTS, Canvas, Memory, Agents
- 📡 **Gateway Proxy** - Route requests through OpenClaw gateway
- 🔄 **Bidirectional Sync** - Keep models/channels in sync

## Installation

The plugin is pre-installed in OpenWebUI Lobster Edition.

## Configuration

Set these environment variables:

```bash
# OpenClaw Gateway
OPENCLAW_GATEWAY_URL=http://localhost:18789
OPENCLAW_GATEWAY_KEY=your-gateway-key

# Or remote (Tailscale)
OPENCLAW_GATEWAY_URL=http://100.106.80.61:18789
```

## Usage

### Models
All OpenClaw models appear in OpenWebUI automatically.

### Authentication
Login with your OpenClaw auth profiles.

### Channels
Send messages through OpenClaw channels (Telegram, WhatsApp, etc.).

### Tools
Use OpenClaw tools directly in chats.

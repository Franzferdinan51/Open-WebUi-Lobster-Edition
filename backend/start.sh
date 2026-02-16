#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit

# =====================
# DuckBot Lobster Edition Custom Config
# =====================
export WEBUI_NAME="Open WebUI Lobster Edition 🦞"

# Default models - include OpenClaw Agent
export DEFAULT_MODELS="openclaw/*,lmstudio/*,minimax-portal/*,openclaw-agent"
export DEFAULT_PINNED_MODELS="openclaw/gpt-5.2,openclaw-agent,lmstudio/qwen3-coder-next,minimax-portal/MiniMax-M2.5"

# OpenClaw Gateway as primary model source
# Add as preset connections (both Ollama and OpenAI-compatible)
export OLLAMA_BASE_URLS="http://localhost:18789"
export OPENAI_API_BASE_URLS="http://localhost:18789/v1"
export OLLAMA_API_BASE_URL="http://localhost:18789/v1"
export OPENAI_API_BASE_URL="http://localhost:18789/v1"
export OPENAI_API_KEY=""

# MiniMax as secondary
# export OPENAI_API_BASE_URL="https://api.minimax.chat/v1"
# export OPENAI_API_KEY="${MINIMAX_API_KEY:-your-minimax-key-here}"

# Enable all DuckBot features
export ENABLE_AGENT_MESH=true
export ENABLE_COMFYUI=true
export ENABLE_CRYPTO=true
export ENABLE_POLYMARKET=true
# =====================

# Add conditional Playwright browser installation
if [[ "${WEB_LOADER_ENGINE,,}" == "playwright" ]]; then
    if [[ -z "${PLAYWRIGHT_WS_URL}" ]]; then
        echo "Installing Playwright browsers..."
        playwright install chromium
        playwright install-deps chromium
    fi

    python -c "import nltk; nltk.download('punkt_tab')"
fi

if [ -n "${WEBUI_SECRET_KEY_FILE}" ]; then
    KEY_FILE="${WEBUI_SECRET_KEY_FILE}"
else
    KEY_FILE=".webui_secret_key"
fi

PORT="${PORT:-8080}"
HOST="${HOST:-0.0.0.0}"
if test "$WEBUI_SECRET_KEY $WEBUI_JWT_SECRET_KEY" = " "; then
  echo "Loading WEBUI_SECRET_KEY from file, not provided as an environment variable."

  if ! [ -e "$KEY_FILE" ]; then
    echo "Generating WEBUI_SECRET_KEY"
    # Generate a random value to use as a WEBUI_SECRET_KEY in case the user didn't provide one.
    echo $(head -c 12 /dev/random | base64) > "$KEY_FILE"
  fi

  echo "Loading WEBUI_SECRET_KEY from $KEY_FILE"
  WEBUI_SECRET_KEY=$(cat "$KEY_FILE")
fi

if [[ "${USE_OLLAMA_DOCKER,,}" == "true" ]]; then
    echo "USE_OLLAMA is set to true, starting ollama serve."
    ollama serve &
fi

if [[ "${USE_CUDA_DOCKER,,}" == "true" ]]; then
  echo "CUDA is enabled, appending LD_LIBRARY_PATH to include torch/cudnn & cublas libraries."
  export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib/python3.11/site-packages/torch/lib:/usr/local/lib/python3.11/site-packages/nvidia/cudnn/lib"
fi

# Check if SPACE_ID is set, if so, configure for space
if [ -n "$SPACE_ID" ]; then
  echo "Configuring for HuggingFace Space deployment"
  if [ -n "$ADMIN_USER_EMAIL" ] && [ -n "$ADMIN_USER_PASSWORD" ]; then
    echo "Admin user configured, creating"
    WEBUI_SECRET_KEY="$WEBUI_SECRET_KEY" uvicorn open_webui.main:app --host "$HOST" --port "$PORT" --forwarded-allow-ips '*' &
    webui_pid=$!
    echo "Waiting for webui to start..."
    while ! curl -s "http://localhost:${PORT}/health" > /dev/null; do
      sleep 1
    done
    echo "Creating admin user..."
    curl \
      -X POST "http://localhost:${PORT}/api/v1/auths/signup" \
      -H "accept: application/json" \
      -H "Content-Type: application/json" \
      -d "{ \"email\": \"${ADMIN_USER_EMAIL}\", \"password\": \"${ADMIN_USER_PASSWORD}\", \"name\": \"Admin\" }"
    echo "Shutting down webui..."
    kill $webui_pid
  fi

  export WEBUI_URL=${SPACE_HOST}
fi

PYTHON_CMD=$(command -v python3 || command -v python)
UVICORN_WORKERS="${UVICORN_WORKERS:-1}"

# If script is called with arguments, use them; otherwise use default workers
if [ "$#" -gt 0 ]; then
    ARGS=("$@")
else
    ARGS=(--workers "$UVICORN_WORKERS")
fi

# Run uvicorn
WEBUI_SECRET_KEY="$WEBUI_SECRET_KEY" exec "$PYTHON_CMD" -m uvicorn open_webui.main:app \
    --host "$HOST" \
    --port "$PORT" \
    --forwarded-allow-ips '*' \
    "${ARGS[@]}"
# OpenClaw Integration - Add to main.py
if ! grep -q "open_webui.plugins.openclaw" backend/open_webui/main.py; then
    echo "Adding OpenClaw plugin to main.py..."
    
    # Add import after other router imports
    sed -i 's/from open_webui.routers import (/from open_webui.routers import (\n    open_webui.plugins.openclaw as openclaw_routers,/' backend/open_webui/main.py
    
    # Add router include after other routers
    sed -i '/app.include_router(skills.router, prefix="\/api\/v1\/skills"/a\
\
# OpenClaw Plugin\
app.include_router(openclaw_routers.models.router, prefix="\/openclaw", tags=["openclaw-models"])\
app.include_router(openclaw_routers.auth.router, prefix="\/openclaw", tags=["openclaw-auth"])\
app.include_router(openclaw_routers.channels.router, prefix="\/openclaw", tags=["openclaw-channels"])\
app.include_router(openclaw_routers.skills.router, prefix="\/openclaw", tags=["openclaw-skills"])' backend/open_webui/start.sh 2>/dev/null
    
    echo "OpenClaw plugin added!"
fi

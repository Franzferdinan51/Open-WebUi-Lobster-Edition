#!/bin/bash
# Watchdog to keep OpenWebUI running

while true; do
    if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "$(date): OpenWebUI down, restarting..."
        cd /home/duckets/open-webui-Lobster-compatable/backend
        source .venv/bin/activate
        pkill -f "uvicorn.*8080" 2>/dev/null
        sleep 2
        nohup python -m uvicorn open_webui.main:app --host 0.0.0.0 --port 8080 > /tmp/openwebui.log 2>&1 &
        echo "$(date): OpenWebUI restarted"
    fi
    sleep 30
done

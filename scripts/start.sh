#!/bin/bash
# Start AI Tokens Service
# Запускает все компоненты системы

echo "🚀 Starting AI Tokens Service..."

# Create directories
mkdir -p ~/.tokens
mkdir -p ~/.logs

# Start token manager
python3 ~/ai-tokens-service/scripts/token_manager.py &
TOKEN_PID=$!
echo "✅ Token Manager started (PID: $TOKEN_PID)"

# Start Telegram bot
if [ -f ~/.env ]; then
    source ~/.env
    if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
        python3 ~/ai-tokens-service/scripts/telegram_bot.py &
        BOT_PID=$!
        echo "✅ Telegram Bot started (PID: $BOT_PID)"
    fi
fi

# Start TON monitor
python3 ~/ai-tokens-service/scripts/ton_monitor.py &
MONITOR_PID=$!
echo "✅ TON Monitor started (PID: $MONITOR_PID)"

# Start OmniRoute proxy
python3 ~/ai-tokens-service/scripts/omniroute_proxy.py &
PROXY_PID=$!
echo "✅ OmniRoute Proxy started (PID: $PROXY_PID)"

echo ""
echo "📊 All services running. Check ~/.logs/ for logs."
echo "🔗 API endpoint: http://localhost:8080/v1/chat/completions"
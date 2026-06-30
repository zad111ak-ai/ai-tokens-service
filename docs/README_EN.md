# AI Tokens Service 💎

**AI Model Monetization Service via TON (The Open Network)**

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/zad111ak-ai/ai-tokens-service/actions/workflows/token-payments.yml/badge.svg)](https://github.com/zad111ak-ai/ai-tokens-service/actions)

## 🎯 What is it?

A ready-to-use solution for selling AI model access through crypto payments:

- **Users** pay TON → receive an API key
- **You** earn on every generation
- **200+ models** via OmniRoute (DeepSeek, Llama, Mistral, GPT, and more)

## 🔧 How It Works

```
User → Telegram Bot → TON Payment → API Key → Model Access
```

| Component | Purpose |
|-----------|---------|
| 🤖 `telegram_bot.py` | User UI: plans, payment, keys |
| 💰 `ton_monitor.py` | Listens to TON blockchain, credits payments |
| 🔑 `token_manager.py` | Issues/revokes API keys (SQLite) |
| 🔄 `omniroute_proxy.py` | Proxy to 200+ models via OmniRoute |

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/zad111ak-ai/ai-tokens-service.git
cd ai-tokens-service

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Set TELEGRAM_BOT_TOKEN, TON_API_KEY

# 4. Run
chmod +x scripts/start.sh
./scripts/start.sh
```

## 📊 Pricing Plans

| Plan | Tokens | Price (TON) | Models |
|------|--------|------------|--------|
| Start | 1000 | 0.5 | Basic |
| Pro | 10000 | 3 | All |
| Enterprise | 100000 | 20 | All + Priority |

## 🏗 24/7 No Server Needed

GitHub Actions checks payments every 5 minutes — no dedicated server required.

## 📚 Documentation

- [Русская версия](../README.md)
- [API Reference](API.md)

## 📜 License

MIT — use freely.

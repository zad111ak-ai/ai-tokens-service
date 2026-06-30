# AI Tokens Service - English Documentation

## Overview
Automated cryptocurrency payment system for AI model access with GitHub Sponsors integration.

## Features
- Accept TON/USDT payments through Telegram bot
- Automatic token distribution to users
- Smart load balancer for cost optimization
- Integration with OmniRoute and Hermes

## Quick Start
```bash
# Clone repository
git clone https://github.com/zad111ak-ai/ai-tokens-service.git
cd ai-tokens-service

# Install dependencies
pip install -r requirements.txt

# Configure tokens
cp .env.example .env
# Fill TELEGRAM_BOT_TOKEN and TON_WALLET

# Start system
python scripts/token_manager.py
python scripts/telegram_bot.py
```

## Token Tiers
- **Basic (1 TON)**: 10,000 tokens
- **Pro (5 TON)**: 60,000 tokens
- **Enterprise (10 TON)**: 250,000 tokens

Tokens = API requests (1 token ≈ 15 characters output)

## Architecture Flow

```
User → Telegram Bot → Payment Verification → Token Granting → AI Model Access
                ↘ GitHub Actions (automated processing)
```

## Integration Points
- **OmniRoute**: Token-gated API endpoints
- **Hermes Agent**: Custom model routing
- **Telegram Bot API**: Payment processing
- **TON API**: Transaction monitoring

## API Endpoints
- `POST /api/balance` - Check user token balance
- `POST /api/grant` - Grant tokens after payment
- `GET /api/models` - Available models by tier

## License
MIT License - Free for personal and commercial use
# API Documentation

## Authentication

All API requests require Bearer token:

```bash
curl -H "Authorization: Bearer ai_your_token_here" \
  http://localhost:8080/v1/chat/completions \
  -d '{"model": "auto/best-coding", "messages": [{"role": "user", "content": "Hello"}]}'
```

## Endpoints

### POST /v1/chat/completions
Chat completions with any available model

### GET /v1/models
List available models (requires token)

### GET /v1/balance
Check your token balance

## Token Pricing

| Tier | Price | Tokens | Models Access |
|------|-------|--------|---------------|
| basic | 1 TON | 10,000 | Free + Groq models |
| pro | 5 TON | 60,000 | All except premium |
| enterprise | 10 TON | 100,000+ | All models including Claude/O1 |

## Usage Examples

```python
import requests

headers = {"Authorization": "Bearer ai_your_key"}

# Chat completion
response = requests.post(
    "http://localhost:8080/v1/chat/completions",
    json={"model": "auto/best-coding", "messages": [{"role": "user", "content": "Write a function"}]},
    headers=headers
)
```

## Webhooks

Telegram bot provides automatic payment processing via `/start` command.
# AI Tokens Service 💎

<p align="center">
  <a href="#russian">🇷🇺 Русский</a> &nbsp;|&nbsp; <a href="#english">🇬🇧 English</a>
</p>

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/zad111ak-ai/ai-tokens-service/actions/workflows/token-payments.yml/badge.svg)](https://github.com/zad111ak-ai/ai-tokens-service/actions)

---

<a id="russian"></a>
## 🇷🇺 О проекте

**Сервис монетизации AI-моделей через крипто-платежи (TON)**

### Что это?

Готовое решение для продажи доступа к AI-моделям:

- **Пользователь** платит TON → получает API-ключ
- **Вы** зарабатываете на каждой генерации
- **200+ моделей** через OmniRoute (DeepSeek, Llama, Mistral, GPT и другие)

### Как работает

```
Пользователь → Telegram Bot → Оплата TON → API ключ → Доступ к моделям
```

| Компонент | Назначение |
|-----------|-----------|
| 🤖 `telegram_bot.py` | UI для пользователей: тарифы, оплата, ключи |
| 💰 `ton_monitor.py` | Слушает блокчейн TON, зачисляет платежи |
| 🔑 `token_manager.py` | Выдаёт/отзывает API-ключи (SQLite) |
| 🔄 `omniroute_proxy.py` | Прокси к 200+ моделям через OmniRoute |

### Быстрый старт

```bash
git clone https://github.com/zad111ak-ai/ai-tokens-service.git
cd ai-tokens-service

pip install -r requirements.txt

cp .env.example .env
# Заполнить TELEGRAM_BOT_TOKEN, TON_API_KEY

chmod +x scripts/start.sh
./scripts/start.sh
```

### Тарифы

| План | Токенов | Цена (TON) | Модели |
|------|---------|-----------|--------|
| Start | 1000 | 0.5 | Базовые |
| Pro | 10000 | 3 | Все |
| Enterprise | 100000 | 20 | Все + приоритет |

### 24/7 без ПК

GitHub Actions проверяет платежи каждые 5 минут — не нужен свой сервер.

---

<a id="english"></a>
## 🇬🇧 About

**Monetize AI models via crypto payments (TON)**

### What is it?

Ready-to-use solution for selling access to AI models:

- **User** pays TON → gets API key
- **You** earn on every generation
- **200+ models** via OmniRoute (DeepSeek, Llama, Mistral, GPT, etc.)

### How it works

```
User → Telegram Bot → TON Payment → API Key → Model Access
```

| Component | Purpose |
|-----------|---------|
| 🤖 `telegram_bot.py` | User UI: plans, payment, keys |
| 💰 `ton_monitor.py` | Listens to TON blockchain, credits payments |
| 🔑 `token_manager.py` | Issues/revokes API keys (SQLite) |
| 🔄 `omniroute_proxy.py` | Proxy to 200+ models via OmniRoute |

### Quick Start

```bash
git clone https://github.com/zad111ak-ai/ai-tokens-service.git
cd ai-tokens-service

pip install -r requirements.txt

cp .env.example .env
# Set TELEGRAM_BOT_TOKEN, TON_API_KEY

chmod +x scripts/start.sh
./scripts/start.sh
```

### Pricing

| Plan | Tokens | Price (TON) | Models |
|------|--------|------------|--------|
| Start | 1000 | 0.5 | Basic |
| Pro | 10000 | 3 | All |
| Enterprise | 100000 | 20 | All + priority |

### 24/7 without a server

GitHub Actions checks payments every 5 minutes — no server needed.

---

## 💸 Donations / Донаты

| Валюта / Currency | Адрес / Address |
|---|---|
| **BTC** | `bc1qd8sa7e4f696wmcyszuxh9snqt2n66zrhz9g80j` |
| **ETH** | `0xD26f0efE6A8F11e127c3Af3D6163BD458a1693c3` |
| **USDT (TON)** | `UQAoI2i8P9-JeZhvGSUwKnymVyY5cb-1Rg7pdqoWMNena7DP` |
| **SOL** | `99EtqBVTeF5UNp9a1oPi18iVXbXptTG7YQ6JeJvXMUJK` |

---

## 📜 License

MIT

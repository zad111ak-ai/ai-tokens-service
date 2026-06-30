# AI Tokens Service 💎

**Сервис монетизации AI-моделей через TON (The Open Network)**

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/zad111ak-ai/ai-tokens-service/actions/workflows/token-payments.yml/badge.svg)](https://github.com/zad111ak-ai/ai-tokens-service/actions)

## 🎯 Что это?

Готовое решение для продажи доступа к AI-моделям через крипто-платежи:

- **Пользователь** платит TON → получает API-ключ
- **Вы** зарабатываете на каждой генерации
- **200+ моделей** через OmniRoute (DeepSeek, Llama, Mistral, GPT и другие)

## 🔧 Как работает

```
Пользователь → Telegram Bot → Оплата TON → API ключ → Доступ к моделям
```

| Компонент | Назначение |
|-----------|-----------|
| 🤖 `telegram_bot.py` | UI для пользователей: тарифы, оплата, ключи |
| 💰 `ton_monitor.py` | Слушает блокчейн TON, зачисляет платежи |
| 🔑 `token_manager.py` | Выдаёт/отзывает API-ключи (SQLite) |
| 🔄 `omniroute_proxy.py` | Прокси к 200+ моделям через OmniRoute |

## 🚀 Быстрый старт

```bash
# 1. Клонировать
git clone https://github.com/zad111ak-ai/ai-tokens-service.git
cd ai-tokens-service

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Настроить
cp .env.example .env
# Заполнить TELEGRAM_BOT_TOKEN, TON_API_KEY

# 4. Запустить
chmod +x scripts/start.sh
./scripts/start.sh
```

## 📊 Тарифы

| План | Токенов | Цена (TON) | Модели |
|------|---------|-----------|--------|
| Start | 1000 | 0.5 | Базовые |
| Pro | 10000 | 3 | Все |
| Enterprise | 100000 | 20 | Все + приоритет |

## 🏗 24/7 Без ПК

GitHub Actions проверяет платежи каждые 5 минут — не нужен свой сервер.

## 📚 Документация

- [English](docs/README_EN.md)
- [API Reference](docs/API.md)

## 📜 Лицензия

MIT — используйте свободно.

# scripts/telegram_bot.py
# Telegram Bot for AI Tokens Service - handles payments and token distribution
# Requires: pip install aiogram python-telegram-bot

import asyncio
import os
import sys
import sqlite3
import time
import hashlib
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or "***"
TON_WALLET = "UQBLEYICSbxKZAajJspddpVYEFtvCcnp7gUpHDZpTChqqAoC"
TOKEN_DB = "~/.tokens/tokens.db"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Токен менеджер
class TokenManager:
    def __init__(self):
        self.db_path = os.path.expanduser(TOKEN_DB)
    
    def grant_tokens(self, telegram_id: str, amount_ton: float) -> tuple:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        tier = "basic" if amount_ton < 5 else ("pro" if amount_ton < 20 else "enterprise")
        tokens = int(amount_ton * 10000)
        
        key = f"ai_{hashlib.sha256(f'{telegram_id}{time.time()}'.encode()).hexdigest()[:32]}"
        
        cur.execute("SELECT tokens FROM users WHERE telegram_id = ?", (telegram_id,))
        row = cur.fetchone()
        
        if row:
            new_tokens = row[0] + tokens
            conn.execute("UPDATE users SET tokens = ? WHERE telegram_id = ?", (new_tokens, telegram_id))
        else:
            conn.execute("INSERT INTO users (telegram_id, tokens, tier) VALUES (?, ?, ?)",
                        (telegram_id, tokens, tier))
        
        conn.commit()
        conn.close()
        return tokens, key

tm = TokenManager()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Купить токены", callback_data="buy_tokens")],
        [InlineKeyboardButton(text="📊 Мой баланс", callback_data="check_balance")]
    ])
    
    await message.answer(
        f"🤖 **AI Tokens Service**\n\n"
        f"Купите токены для доступа к AI моделям:\n\n"
        f"• 1 TON = 10,000 токенов\n"
        f"• Мгновенная выдача после оплаты\n"
        f"• Доступ к 200+ моделям\n\n"
        f"💳 Кошелёк: `{TON_WALLET}`\n\n"
        f"Нажмите кнопку ниже для покупки",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.callback_query(lambda c: c.data == "buy_tokens")
async def process_buy(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 TON (10K токенов)", callback_data="buy_1")],
        [InlineKeyboardButton(text="5 TON (50K токенов)", callback_data="buy_5")],
        [InlineKeyboardButton(text="10 TON (100K токенов)", callback_data="buy_10")]
    ])
    
    await callback.message.edit_text(
        f"💰 Выберите количество токенов:\n\n"
        f"После оплаты отправьте TX hash боту",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def process_purchase(callback: types.CallbackQuery):
    amount = int(callback.data.split("_")[1])
    tx_id = f"tx_{time.time()}_{callback.from_user.id}"
    
    # Генерируем временную запись о покупке
    await callback.message.edit_text(
        f"🔄 **Ожидаем подтверждения оплаты**\n\n"
        f"Сумма: {amount} TON\n"
        f"TX ID: `{tx_id}`\n\n"
        f"Отправьте TON на кошелёк: `{TON_WALLET}`\n"
        f"И напишите: /confirm_{tx_id}\n\n"
        f"_После подтверждения вы получите API ключ_",
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    print("✅ Telegram Bot initialized")
    asyncio.run(dp.start_polling(bot))
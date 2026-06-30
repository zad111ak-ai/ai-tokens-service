#!/usr/bin/env python3
"""
TON Payment Monitor for AI Tokens Service
Мониторинг транзакций TON и выдача токенов
"""

import asyncio
import aiohttp
import sqlite3
import time
import hashlib
import os
import json
from typing import Optional

# Configuration
TON_API_KEY = os.getenv('TON_API_KEY')
TON_WALLET = "UQBLEYICSbxKZAajJspddpVYEFtvCcnp7gUpHDZpTChqqAoC"
TOKEN_DB = os.path.expanduser('~/.tokens/tokens.db')

class TONMonitor:
    def __init__(self):
        self.api_url = "https://tontenter.org/api/v3"
        self.last_tx_time = time.time()
    
    async def fetch_transactions(self) -> list:
        """Get recent transactions for the wallet"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/transactions",
                params={"address": TON_WALLET, "limit": 20, "offset": 0}
            ) as resp:
                data = await resp.json()
                return data.get('transactions', [])
    
    def record_payment(self, tx_hash: str, telegram_id: int, amount: float):
        """Record payment in database"""
        conn = sqlite3.connect(TOKEN_DB)
        conn.execute("""INSERT OR IGNORE INTO transactions 
                        (tx_hash, telegram_id, amount_ton, tokens_granted, timestamp)
                        VALUES (?, ?, ?, ?, ?)""",
                     (tx_hash, str(telegram_id), amount, int(amount * 10000), time.time()))
        conn.commit()
        conn.close()
        
        # Grant tokens
        from token_manager import TokenManager
        tm = TokenManager()
        tokens, api_key = tm.grant_tokens(str(telegram_id), amount)
        
        print(f"✅ Granted {tokens} tokens to {telegram_id}")
        return tokens, api_key
    
    async def monitor(self):
        """Main monitoring loop"""
        while True:
            try:
                txs = await self.fetch_transactions()
                for tx in txs:
                    if tx.get('value', 0) > 0 and tx.get('status') == 'paid':
                        comment = tx.get('comment', '')
                        # Extract telegram ID from comment (format: "telegram:123456")
                        if 'telegram:' in comment:
                            telegram_id = comment.split('telegram:')[1].split('_')[0]
                            amount = float(tx.get('value', 0)) / 1e9  # Convert to TON
                            self.record_payment(tx['hash'], telegram_id, amount)
            except Exception as e:
                print(f"⚠️ Error: {e}")
            
            await asyncio.sleep(60)  # Check every minute

if __name__ == "__main__":
    monitor = TONMonitor()
    print("✅ TON Payment Monitor started")
    asyncio.run(monitor.monitor())
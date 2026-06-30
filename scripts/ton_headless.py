#!/usr/bin/env python3
"""
Headless TON Monitor for GitHub Actions
Запускается каждые 5 минут в GitHub Actions
"""

import asyncio
import aiohttp
import sqlite3
import time
import hashlib
import os
import argparse

TON_API_KEY = os.getenv('TON_API_KEY')
TON_WALLET = "UQBLEYICSbxKZAajJspddpVYEFtvCcnp7gUpHDZpTChqqAoC"
TOKEN_DB = os.path.expanduser('~/.tokens/tokens.db')

async def check_payments():
    """Check transactions and grant tokens (headless mode)"""
    if not TON_API_KEY:
        print("⚠️ TON_API_KEY not set")
        return
        
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                "https://tontenter.org/api/v3/transactions",
                params={"address": TON_WALLET, "limit": 20}
            ) as resp:
                data = await resp.json()
                
                for tx in data.get('transactions', []):
                    if tx.get('value', 0) > 0:
                        comment = tx.get('comment', '')
                        if 'telegram:' in comment:
                            telegram_id = comment.split('telegram:')[1].split('_')[0]
                            amount = float(tx.get('value', 0)) / 1e9
                            
                            # Update database
                            conn = sqlite3.connect(TOKEN_DB)
                            cur = conn.cursor()
                            
                            cur.execute("SELECT tokens FROM users WHERE telegram_id = ?", (telegram_id,))
                            row = cur.fetchone()
                            
                            tier = "basic" if amount < 5 else ("pro" if amount < 20 else "enterprise")
                            
                            if row:
                                new_tokens = row[0] + int(amount * 10000)
                                conn.execute("UPDATE users SET tokens = ? WHERE telegram_id = ?", (new_tokens, telegram_id))
                            else:
                                new_tokens = int(amount * 10000)
                                conn.execute("INSERT INTO users (telegram_id, tokens, tier) VALUES (?, ?, ?)",
                                            (telegram_id, new_tokens, tier))
                            
                            # Generate API key
                            api_key = f"ai_{hashlib.sha256(f'{telegram_id}{time.time()}'.encode()).hexdigest()[:32]}"
                            conn.execute("INSERT INTO api_keys (key_hash, telegram_id, created_at, expires_at, tier) VALUES (?, ?, ?, ?, ?)",
                                        (hashlib.sha256(api_key.encode()).hexdigest(), telegram_id, time.time(), time.time() + 86400*30, tier))
                            
                            conn.commit()
                            conn.close()
                            
                            print(f"✅ Granted {new_tokens} tokens to {telegram_id}")
                            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="Run once and exit")
    args = parser.parse_args()
    
    if args.check_only:
        asyncio.run(check_payments())
    else:
        while True:
            asyncio.run(check_payments())
            time.sleep(60)
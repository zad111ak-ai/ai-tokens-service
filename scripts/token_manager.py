#!/usr/bin/env python3
"""
AI Tokens Service - Token Management and Payment Processing
Система управления токенами для доступа к AI моделям через OmniRoute
"""

import sqlite3
import hashlib
import time
import json
import os
import threading
from typing import Optional
from contextlib import contextmanager

class TokenManager:
    def __init__(self, db_path="~/.tokens/tokens.db"):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._lock = threading.Lock()
        self.init_db()
    
    @contextmanager
    def _get_conn(self):
        """Thread-safe database connection"""
        with self._lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
            finally:
                conn.close()
    
    def init_db(self):
        with self._get_conn() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS users (
                telegram_id TEXT PRIMARY KEY,
                tokens INTEGER DEFAULT 0,
                used_tokens INTEGER DEFAULT 0,
                expires_at REAL,
                tier TEXT
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS transactions (
                tx_hash TEXT PRIMARY KEY,
                telegram_id TEXT,
                amount_ton REAL,
                tokens_granted INTEGER,
                timestamp REAL
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS api_keys (
                key_hash TEXT PRIMARY KEY,
                telegram_id TEXT,
                created_at REAL,
                expires_at REAL,
                tier TEXT
            )""")
            conn.commit()
    
    def generate_api_key(self, telegram_id: str, tier: str = "basic") -> str:
        key = f"ai_{hashlib.sha256(f'{telegram_id}{time.time()}'.encode()).hexdigest()[:32]}"
        expires = time.time() + (30 * 24 * 3600)  # 30 дней
        
        with self._get_conn() as conn:
            conn.execute("""INSERT INTO api_keys (key_hash, telegram_id, created_at, expires_at, tier)
                          VALUES (?, ?, ?, ?, ?)""",
                       (hashlib.sha256(key.encode()).hexdigest(), telegram_id, time.time(), expires, tier))
            conn.commit()
        return key
    
    def grant_tokens(self, telegram_id: str, amount_ton: float) -> tuple[int, str]:
        tier = "basic" if amount_ton < 5 else ("pro" if amount_ton < 20 else "enterprise")
        
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT tokens FROM users WHERE telegram_id = ?", (telegram_id,))
            row = cur.fetchone()
            
            if row:
                new_tokens = row[0] + int(amount_ton * 10000)
                conn.execute("UPDATE users SET tokens = ? WHERE telegram_id = ?", (new_tokens, telegram_id))
            else:
                new_tokens = int(amount_ton * 10000)
                conn.execute("INSERT INTO users (telegram_id, tokens, tier) VALUES (?, ?, ?)",
                            (telegram_id, new_tokens, tier))
            conn.commit()
        
        api_key = self.generate_api_key(telegram_id, tier)
        return new_tokens, api_key
    
    def check_balance(self, telegram_id: str) -> dict:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT tokens, used_tokens, tier, expires_at FROM users WHERE telegram_id = ?", (telegram_id,))
            row = cur.fetchone()
        
        if row:
            return {"total": row[0], "used": row[1], "remaining": row[0] - row[1], "tier": row[2], "expires": row[3]}
        return {"total": 0, "used": 0, "remaining": 0, "tier": "none", "expires": 0}

if __name__ == "__main__":
    tm = TokenManager()
    print("✅ Token Manager initialized")
    print("📊 Current users:", len(os.listdir(os.path.expanduser("~/.tokens"))))
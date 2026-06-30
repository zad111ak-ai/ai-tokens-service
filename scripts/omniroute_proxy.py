#!/usr/bin/env python3
"""
OmniRoute Proxy with Token Validation
Прокси для доступа к AI моделям с проверкой токенов
"""

import os
import sys
import time
import aiohttp
from aiohttp import web

# Configuration
OMNIROUTE_URL = os.getenv('OMNIROUTE_URL', 'http://localhost:20128')
TOKEN_DB = os.path.expanduser('~/.tokens/tokens.db')

async def validate_token(request):
    """Extract and validate token from request"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header[7:]
    import sqlite3
    import hashlib
    
    conn = sqlite3.connect(TOKEN_DB)
    cur = conn.cursor()
    cur.execute("SELECT telegram_id, expires_at FROM api_keys WHERE key_hash = ?",
                (hashlib.sha256(token.encode()).hexdigest(),))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return None
    
    if row[1] and row[1] < time.time():
        return None
    
    return row[0]

async def proxy_request(request):
    telegram_id = await validate_token(request)
    if not telegram_id:
        return web.json_response({"error": "Invalid or expired token"}, status=401)
    
    # Forward to OmniRoute
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=request.method,
            url=f"{OMNIROUTE_URL}{request.path}",
            headers=dict(request.headers),
            data=await request.read()
        ) as resp:
            return web.json_response(await resp.json())

if __name__ == "__main__":
    app = web.Application()
    app.router.add_route('*', '/{path:.*}', proxy_request)
    web.run_app(app, port=8080)
    print("✅ OmniRoute Token Proxy running on port 8080")
#!/usr/bin/env python3
"""
Test Supabase connection
"""

import httpx
from pathlib import Path

# Load .env
SUPABASE_URL = "https://sktrmwogifeuzrcnpvsw.supabase.co"
SUPABASE_KEY = ""

env_file = Path("/Users/franciscotaveira.ads/LUNA OS/.env")
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                if key == 'SUPABASE_KEY':
                    SUPABASE_KEY = value

print(f"✅ SUPABASE_KEY: {SUPABASE_KEY[:20]}...")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

# Test 1: Simple query
print("\n📊 Test 1: Simple query...")
try:
    url = f"{SUPABASE_URL}/rest/v1/whatsapp_messages_history"
    params = {"limit": 5}
    
    response = httpx.get(url, headers=headers, params=params, timeout=30)
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Success! {len(data)} rows returned")
        if data:
            print(f"   Keys: {list(data[0].keys())}")
    else:
        print(f"   ❌ Error: {response.text[:200]}")
        
except Exception as e:
    print(f"   ❌ Exception: {e}")

print("\n✅ Test completed")

#!/usr/bin/env python3
"""
🌙💼 LUNA OS — REAL CUSTOMER SCHEDULING MINING
Busca mensagens INBOUND (das clientes) com situações REAIS de agendamento
"""

import httpx
import json
from pathlib import Path
from datetime import datetime

# Carregar creds do .env
env_file = Path('/Users/franciscotaveira.ads/LUNA OS/.env')
SUPABASE_URL = ''
SUPABASE_KEY = ''

if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                if key == 'SUPABASE_URL':
                    SUPABASE_URL = value
                elif key == 'SUPABASE_KEY':
                    SUPABASE_KEY = value

HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}'
}

print("\n")
print("╔════════════════════════════════════════════════════╗")
print("║  🌙 BUSCANDO SITUAÇÕES REAIS DE CLIENTES         ║")
print("║     Apenas mensagens INBOUND (das clientes)       ║")
print("╚════════════════════════════════════════════════════╝")
print()

# Keywords que indicam situações complexas REAIS de clientes
complex_keywords = [
    'encaixar',
    'consegue',
    'tem horário',
    'ocupada',
    'finalizando',
    'esperar',
    'aguardar',
    'também quero',
    'além de',
    'demora quanto',
    'pressa',
    'urgente',
    'outro dia',
    'não tem',
    'lotado',
    'qual horário',
    'pode ser',
]

all_situations = []

for keyword in complex_keywords:
    try:
        response = httpx.get(
            f'{SUPABASE_URL}/rest/v1/whatsapp_messages_history',
            headers=HEADERS,
            params={
                'content.ilike': f'%{keyword}%',
                'direction': 'inbound',
                'limit': 10
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            msgs = response.json()
            if msgs:
                print(f'✅ "{keyword}": {len(msgs)} mensagens de clientes')
                for msg in msgs[:2]:
                    content = msg.get('content', '')
                    phone = msg.get('phone', '?')
                    timestamp = msg.get('message_timestamp', '')
                    
                    print(f'   📱 {phone} ({timestamp[:16] if timestamp else "?"})')
                    print(f'   "{content[:180]}..."')
                    print()
                    
                    all_situations.append({
                        'keyword': keyword,
                        'phone': phone,
                        'timestamp': timestamp,
                        'content': content,
                        'direction': 'inbound'
                    })
    except Exception as e:
        print(f'   ❌ "{keyword}": {e}')

print()
print("─" * 70)
print(f"📊 TOTAL: {len(all_situations)} situações reais encontradas")
print()

# Salvar
if all_situations:
    output_file = Path('/Users/franciscotaveira.ads/LUNA OS/logs/real_customer_situations.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_situations, f, indent=2, ensure_ascii=False)
    print(f'💾 Salvo em: {output_file}')
    print()

print("✅ Busca concluída!")

#!/usr/bin/env python3
"""
🌙📥 LUNA OS v3.0 — EXTRAÇÃO DIRETA DE CONVERSAS
Versão simplificada que extrai sem count
"""

import httpx
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
from loguru import logger

# Config
SUPABASE_URL = "https://sktrmwogifeuzrcnpvsw.supabase.co"
SUPABASE_KEY = ""

# Load .env
env_file = Path("/Users/franciscotaveira.ads/LUNA OS/.env")
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                if key == 'SUPABASE_KEY':
                    SUPABASE_KEY = value

logger.info(f"✅ SUPABASE_KEY loaded ({len(SUPABASE_KEY)} chars)")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

output_dir = Path("/Users/franciscotaveira.ads/LUNA OS/logs/extractions")
output_dir.mkdir(parents=True, exist_ok=True)

logger.info()
logger.info("╔════════════════════════════════════════════════════╗")
logger.info("║  📥 EXTRAÇÃO DIRETA DE CONVERSAS                  ║")
logger.info("╚════════════════════════════════════════════════════╝")
logger.info()

# Extract messages (filter out groups)
logger.info("📥 Extracting messages from Supabase (excluding groups)...")
logger.info("─" * 50)

all_messages = []
offset = 0  # Start from beginning
batch_size = 5000
max_batches = 200

start_time = time.time()

for batch_num in range(max_batches):
    try:
        url = f"{SUPABASE_URL}/rest/v1/whatsapp_messages_history"
        params = {"limit": batch_size, "offset": offset, "is_group": "eq.false"}

        # Retry logic for 502/503 errors
        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            response = httpx.get(url, headers=headers, params=params, timeout=300)

            if response.status_code in [502, 503, 504]:
                if attempt < max_retries - 1:
                    logger.info(f"   ⚠️  Batch {batch_num + 1}: Status {response.status_code} - Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    logger.info(f"   ❌ Batch {batch_num + 1}: Status {response.status_code} after {max_retries} retries")
                    break
            else:
                break

        if response.status_code != 200:
            logger.info(f"   ❌ Batch {batch_num + 1}: Status {response.status_code}")
            break

        messages = response.json()

        if not messages:
            logger.info(f"   ✅ Batch {batch_num + 1}: No more data")
            break

        all_messages.extend(messages)
        offset += len(messages)

        elapsed = time.time() - start_time
        rows_per_sec = len(all_messages) / elapsed if elapsed > 0 else 0

        logger.info(f"   ✅ Batch {batch_num + 1}: {len(messages):,} rows (total: {len(all_messages):,}) - {rows_per_sec:.1f} rows/sec")

        # Rate limiting (reduced for faster extraction)
        time.sleep(0.2)

    except Exception as e:
        logger.info(f"   ❌ Batch {batch_num + 1}: Error - {e}")
        break

elapsed = time.time() - start_time

logger.info()
logger.info(f"✅ Extraction completed: {len(all_messages):,} messages in {elapsed:.1f}s")
logger.info()

# Group by phone
logger.info("📊 Grouping by phone...")
logger.info("─" * 50)

conversations = defaultdict(list)

for msg in all_messages:
    phone = msg.get("phone", "unknown")
    conversations[phone].append(msg)

# Sort messages within each conversation
for phone in conversations:
    conversations[phone] = sorted(
        conversations[phone],
        key=lambda x: x.get("message_timestamp", "")
    )

logger.info(f"✅ {len(conversations):,} conversations grouped")
logger.info()

# Calculate stats
logger.info("📊 Calculating statistics...")
logger.info("─" * 50)

conversation_stats = []

for phone, msgs in conversations.items():
    inbound = [m for m in msgs if m.get("direction") == "inbound"]
    outbound = [m for m in msgs if m.get("direction") == "outbound"]
    
    # Duration
    if msgs:
        t1 = msgs[0].get("message_timestamp", "")
        t2 = msgs[-1].get("message_timestamp", "")
        
        try:
            dt1 = datetime.fromisoformat(t1.replace("Z", "+00:00"))
            dt2 = datetime.fromisoformat(t2.replace("Z", "+00:00"))
            duration_minutes = (dt2 - dt1).total_seconds() / 60
        except Exception as e:
            # [DEBT #A9] Manter fallback mas logar erro específico
            logger.debug(f"Erro ao calcular duração: {e}")
            duration_minutes = 0
    else:
        duration_minutes = 0
    
    conversation_stats.append({
        "phone": phone,
        "total_messages": len(msgs),
        "inbound_count": len(inbound),
        "outbound_count": len(outbound),
        "duration_minutes": duration_minutes,
        "first_message": t1 if msgs else None,
        "last_message": t2 if msgs else None,
        "first_content": inbound[0].get("content", "")[:100] if inbound else "",
        "last_content": msgs[-1].get("content", "")[:100] if msgs else ""
    })

# Sort by message count
conversation_stats = sorted(
    conversation_stats,
    key=lambda x: x["total_messages"],
    reverse=True
)

# Stats
stats = {
    "total_conversations": len(conversation_stats),
    "total_messages": len(all_messages),
    "conversations_with_10_plus": sum(1 for c in conversation_stats if c["total_messages"] >= 10),
    "conversations_with_50_plus": sum(1 for c in conversation_stats if c["total_messages"] >= 50),
    "conversations_with_100_plus": sum(1 for c in conversation_stats if c["total_messages"] >= 100)
}

logger.info(f"📊 STATISTICS:")
logger.info(f"   • Total Conversations: {stats['total_conversations']:,}")
logger.info(f"   • Total Messages: {stats['total_messages']:,}")
logger.info(f"   • 10+ messages: {stats['conversations_with_10_plus']:,}")
logger.info(f"   • 50+ messages: {stats['conversations_with_50_plus']:,}")
logger.info(f"   • 100+ messages: {stats['conversations_with_100_plus']:,}")
logger.info()

# Save
logger.info("💾 Saving conversations...")
logger.info("─" * 50)

timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
output_file = output_dir / f"whatsapp_conversations_{timestamp}.json"

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        "metadata": {
            "extracted_at": timestamp,
            "source": "Supabase",
            "table": "whatsapp_messages_history",
            **stats
        },
        "conversations": conversation_stats
    }, f, indent=2, ensure_ascii=False)

logger.info(f"✅ Saved to: {output_file}")
logger.info()

# Save top 10 conversations as TXT
txt_file = output_dir / f"top_conversations_{timestamp}.txt"

with open(txt_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("LUNA OS — TOP CONVERSAS DO WHATSAPP\n")
    f.write(f"Extraído em: {timestamp}\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"ESTATÍSTICAS:\n")
    f.write(f"  Total Conversas: {stats['total_conversations']:,}\n")
    f.write(f"  Total Mensagens: {stats['total_messages']:,}\n")
    f.write(f"  10+ mensagens: {stats['conversations_with_10_plus']:,}\n")
    f.write(f"  50+ mensagens: {stats['conversations_with_50_plus']:,}\n")
    f.write(f"  100+ mensagens: {stats['conversations_with_100_plus']:,}\n")
    f.write("\n" + "=" * 80 + "\n\n")
    
    for i, conv in enumerate(conversation_stats[:10], 1):
        f.write(f"\n{'='*80}\n")
        f.write(f"CONVERSA #{i} — {conv['phone']}\n")
        f.write(f"{'='*80}\n")
        f.write(f"Mensagens: {conv['total_messages']}\n")
        f.write(f"Duração: {conv['duration_minutes']:.0f} minutos\n")
        f.write(f"Início: {conv['first_message']}\n")
        f.write(f"Fim: {conv['last_message']}\n")
        f.write(f"\nPRIMEIRA MENSAGEM:\n{conv['first_content']}\n")
        f.write(f"\nÚLTIMA MENSAGEM:\n{conv['last_content']}\n")
        f.write(f"{'-'*80}\n")

logger.info(f"✅ Saved TXT to: {txt_file}")
logger.info()

logger.info("╔════════════════════════════════════════════════════╗")
logger.info("║  ✅ EXTRAÇÃO COMPLETA CONCLUÍDA                   ║")
logger.info("╚════════════════════════════════════════════════════╝")
logger.info()
logger.info(f"📁 Arquivos:")
logger.info(f"   • JSON: {output_file}")
logger.info(f"   • TXT: {txt_file}")
logger.info()

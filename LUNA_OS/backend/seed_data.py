import os
import asyncio
from datetime import datetime, timedelta
from app.integrations.supabase_client import get_supabase


async def seed():
    print("🌱 Seeding Truth in Data...")
    db = get_supabase()

    # Create a test conversation
    now = datetime.utcnow().isoformat()
    conv = {
        "status": "active",
        "phone": "5500000000000",
        "started_at": now,
        "intent": "agendamento",
    }
    db.table("conversations").insert(conv).execute()

    # Create a test message
    msg = {
        "direction": "inbound",
        "content": "Quero agendar uma consulta",
        "created_at": now,
        "response_time_ms": 1500,
    }
    db.table("messages").insert(msg).execute()

    print("✅ Seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
